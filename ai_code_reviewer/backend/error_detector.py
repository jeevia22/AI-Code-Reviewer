import ast
import builtins


# All Python builtins so we never flag them as "undefined"
_BUILTINS = set(dir(builtins))


class _Reviewer(ast.NodeVisitor):
    def __init__(self):
        self.defined = set()
        self.used    = set()
        self.imports = set()
        self.issues  = []
        self._func_names = set()

    # ── Imports ───────────────────────────────────────────────────────────
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]
            self.imports.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports.add(name)
        self.generic_visit(node)

    # ── Functions ─────────────────────────────────────────────────────────
    def visit_FunctionDef(self, node):
        self._func_names.add(node.name)
        self.defined.add(node.name)

        # Register all arguments as defined
        for arg in node.args.args:
            self.defined.add(arg.arg)
        if node.args.vararg:
            self.defined.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.defined.add(node.args.kwarg.arg)
        for arg in node.args.kwonlyargs:
            self.defined.add(arg.arg)

        # ── Mutable default arguments ─────────────────────────────────────
        for default in node.args.defaults + node.args.kw_defaults:
            if default and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append({
                    "type": "Mutable Default Argument",
                    "line": node.lineno,
                    "message": (
                        f"'{node.name}' uses a mutable default argument "
                        f"({type(default).__name__}). Use None and assign inside the function."
                    ),
                })

        # ── Parameters that shadow builtins ───────────────────────────────
        for arg in node.args.args:
            if arg.arg in _BUILTINS:
                self.issues.append({
                    "type": "Builtin Shadow",
                    "line": node.lineno,
                    "message": (
                        f"Parameter '{arg.arg}' in '{node.name}' shadows a Python builtin."
                    ),
                })

        # ── Infinite recursion (recursive call with no conditional guard) ─
        recursive_call = any(
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Name)
            and child.func.id == node.name
            for child in ast.walk(node)
        )
        if recursive_call:
            has_if = any(isinstance(n, ast.If) for n in ast.walk(node))
            if not has_if:
                self.issues.append({
                    "type": "Infinite Recursion",
                    "line": node.lineno,
                    "message": (
                        f"'{node.name}' calls itself recursively with no base-case condition."
                    ),
                })

        self.generic_visit(node)

    # AsyncDef gets the same treatment
    visit_AsyncFunctionDef = visit_FunctionDef

    # ── Variables ─────────────────────────────────────────────────────────
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    # ── Infinite while loops ──────────────────────────────────────────────
    def visit_While(self, node):
        is_while_true = (
            isinstance(node.test, ast.Constant) and node.test.value is True
        ) or (
            isinstance(node.test, ast.NameConstant) and node.test.value is True
        )
        if is_while_true:
            has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
            if not has_break:
                self.issues.append({
                    "type": "Infinite Loop",
                    "line": node.lineno,
                    "message": "while True loop has no break statement — will run forever.",
                })
        self.generic_visit(node)

    # ── Bare except ───────────────────────────────────────────────────────
    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.issues.append({
                "type": "Bare Except",
                "line": node.lineno,
                "message": (
                    "Bare `except:` catches ALL exceptions including SystemExit and "
                    "KeyboardInterrupt. Use `except Exception:` or a specific type."
                ),
            })
        self.generic_visit(node)

    # ── Analyse collected data ────────────────────────────────────────────
    def analyze(self):
        all_defined = self.defined | self.imports | _BUILTINS | self._func_names
        results = list(self.issues)  # already has line numbers

        # Unused variables (exclude _ convention)
        for var in sorted(self.defined - self.used):
            if not var.startswith("_"):
                results.append({
                    "type": "Unused Variable",
                    "message": f"'{var}' is defined but never used.",
                })

        # Unused imports
        for imp in sorted(self.imports - self.used):
            results.append({
                "type": "Unused Import",
                "message": f"'{imp}' is imported but never used.",
            })

        return results


def detect_errors(code: str) -> list:
    """
    Run static analysis on already-validated Python code.
    Call parse_code() first — this function assumes the code is syntactically valid.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{"type": "SyntaxError", "message": str(e)}]

    reviewer = _Reviewer()
    reviewer.visit(tree)
    return reviewer.analyze()