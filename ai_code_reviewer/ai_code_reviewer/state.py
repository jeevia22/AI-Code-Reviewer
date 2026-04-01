import reflex as rx
from backend.code_parser import parse_code
from backend.error_detector import detect_errors
from backend.ai_suggester import get_ai_suggestion

BLANK_SYNTAX  = "— run analysis to see results —"
BLANK_ERRORS  = "— run analysis to see results —"
BLANK_AI      = "— run analysis to see AI suggestions —"
BLANK_IMPROVED = "— improved code will appear here after analysis —"


class State(rx.State):
    user_code: str = ""
    syntax_output: str = BLANK_SYNTAX
    errors_output: str = BLANK_ERRORS
    ai_output: str = BLANK_AI
    improved_code: str = BLANK_IMPROVED
    is_loading: bool = False

    def set_user_code(self, value: str):
        self.user_code = value

    def reset_editor(self):
        """Clear everything back to initial state."""
        self.user_code     = ""
        self.syntax_output  = BLANK_SYNTAX
        self.errors_output  = BLANK_ERRORS
        self.ai_output      = BLANK_AI
        self.improved_code  = BLANK_IMPROVED
        self.is_loading     = False

    def analyze_code(self):
        if not self.user_code.strip():
            self.syntax_output = "⚠  No code provided."
            self.errors_output = ""
            self.ai_output     = ""
            self.improved_code = ""
            return

        self.is_loading     = True
        self.syntax_output  = "Analyzing…"
        self.errors_output  = "…"
        self.ai_output      = "Waiting for AI…"
        self.improved_code  = "Generating improved code…"

        # 1. Syntax check
        result = parse_code(self.user_code)
        if not result["success"]:
            msg    = result["error"]["message"]
            lineno = result["error"].get("lineno", "")
            loc    = f" (line {lineno})" if lineno else ""
            self.syntax_output = f"✗ Syntax Error{loc}:\n  {msg}"
            self.errors_output = "Analysis stopped — fix syntax error first."
            self.ai_output     = ""
            self.improved_code = ""
            self.is_loading    = False
            return

        self.syntax_output = "✓ No syntax errors found."

        # 2. Static analysis
        errors = detect_errors(self.user_code)
        if errors:
            self.errors_output = "\n".join(
                f"  {e['type']}: {e.get('message', '')}" for e in errors
            )
        else:
            self.errors_output = "✓ No issues detected."

        # 3. AI suggestions (natural language)
        raw = get_ai_suggestion(self.user_code, errors)
        self.ai_output = raw.replace("**", "").replace("*", "").strip()

        # 4. AI-rewritten improved code
        improved_prompt = (
            "Rewrite the following Python code fixing ALL detected issues: "
            "remove unused imports, remove unused variables, fix infinite loops, "
            "replace bare excepts with specific exceptions, fix mutable default arguments, "
            "rename parameters that shadow builtins. "
            "Return ONLY the corrected Python code. No explanation. No markdown fences.\n\n"
            f"Original code:\n{self.user_code}"
        )
        try:
            raw_improved = get_ai_suggestion(improved_prompt, [])
            cleaned = raw_improved.strip()
            if cleaned.startswith("```"):
                lines = [l for l in cleaned.split("\n") if not l.strip().startswith("```")]
                cleaned = "\n".join(lines).strip()
            self.improved_code = cleaned
        except Exception:
            self.improved_code = "# Could not generate improved code."

        self.is_loading = False