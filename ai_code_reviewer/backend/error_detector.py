import ast


class AIReviewer(ast.NodeVisitor):
    def __init__(self):
        self.defined = set()
        self.used = set()
        self.imports = set()
        self.issues = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            self.defined.add(arg.arg)

        function_name = node.name
        recursive_call = False

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == function_name:
                    recursive_call = True

        if recursive_call:
            has_if = any(isinstance(n, ast.If) for n in ast.walk(node))
            if not has_if:
                self.issues.append({
                    "type": "Infinite Recursion",
                    "line": node.lineno,
                    "message": "Recursive function without base condition."
                })

        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
            if not has_break:
                self.issues.append({
                    "type": "Infinite Loop",
                    "line": node.lineno,
                    "message": "while True without break."
                })
        self.generic_visit(node)

    def analyze(self):
        undefined_vars = self.used - self.defined - set(dir(__builtins__))
        unused_vars = self.defined - self.used
        unused_imports = self.imports - self.used

        results = []

        for var in undefined_vars:
            results.append({
                "type": "Undefined Variable",
                "message": f"{var} is not defined."
            })

        for var in unused_vars:
            results.append({
                "type": "Unused Variable",
                "message": f"{var} is defined but not used."
            })

        for imp in unused_imports:
            results.append({
                "type": "Unused Import",
                "message": f"{imp} is imported but not used."
            })

        results.extend(self.issues)

        return results


def detect_errors(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{"type": "Syntax Error", "message": str(e)}]

    reviewer = AIReviewer()
    reviewer.visit(tree)
    return reviewer.analyze()