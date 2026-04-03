import os
from groq import Groq

# ── API key resolution ────────────────────────────────────────────────────────
# Works in ALL environments:
#   • Local dev  → reads from .env via python-dotenv (loaded in rxconfig.py)
#   • reflex deploy → reads secret injected as GROQ_API_KEY environment variable
#
# Do NOT call load_dotenv() here. Load it once at app startup in rxconfig.py so
# the variable is in os.environ before this module is imported.
# ─────────────────────────────────────────────────────────────────────────────

_client = None


def _get_client() -> Groq | None:
    global _client
    if _client is not None:
        return _client
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print(
            "[ai_suggester] WARNING: GROQ_API_KEY is not set. "
            "Add it to your .env file locally, or run:\n"
            "  reflex deploy --env GROQ_API_KEY=<your-key>"
        )
        return None
    try:
        _client = Groq(api_key=api_key)
        return _client
    except Exception as e:
        print(f"[ai_suggester] Groq client init error: {e}")
        return None


# ── System prompts ────────────────────────────────────────────────────────────
_REVIEW_SYSTEM = """You are a senior Python engineer and code reviewer who thinks like the CPython compiler + pylint combined.

When given Python code and a list of detected static-analysis issues, you must:
1. Explain every detected issue clearly, referencing line numbers where possible.
2. Give a concrete corrected snippet for each issue.
3. Analyse time complexity and space complexity.
4. Check PEP 8 naming conventions (variables, functions, classes).
5. Suggest best practices: type hints, docstrings, guard clauses, etc.

Be precise and technical. Never hallucinate errors that aren't there.
Do NOT wrap your answer in markdown code fences."""

_IMPROVE_SYSTEM = """You are an expert Python programmer. Your only job is to rewrite the given Python code to fix ALL detected issues:
- Remove unused imports and unused variables
- Fix infinite loops by adding a proper break or return condition
- Replace bare `except:` with specific exception types (e.g. `except ValueError:`)
- Fix mutable default arguments (e.g. `def f(x=[])` → `def f(x=None)` with guard)
- Rename parameters that shadow builtins (e.g. `list`, `input`, `id`)
- Keep all logic identical — only fix the flagged issues

Return ONLY the corrected Python code. No explanation. No markdown fences. No commentary."""


# ── Public API ────────────────────────────────────────────────────────────────
def get_ai_suggestion(code: str, detected_errors: list) -> str:
    """Return natural-language review of the code."""
    client = _get_client()
    if client is None:
        return (
            "\u26a0  GROQ_API_KEY not set.\n\n"
            "Local: add GROQ_API_KEY=<key> to your .env file.\n"
            "Deploy: reflex deploy --env GROQ_API_KEY=<key>"
        )

    formatted_errors = "\n".join(
        f"- {e['type']}: {e.get('message', '')}" for e in detected_errors
    ) or "None detected by static analysis."

    user_msg = (
        f"Detected Issues:\n{formatted_errors}\n\n"
        f"Code:\n{code}"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": _REVIEW_SYSTEM},
                {"role": "user",   "content": user_msg},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"[ai_suggester] Groq API error: {e}")
        return f"\u26a0  AI service error: {e}"


def get_improved_code(code: str, detected_errors: list) -> str:
    """Return only the rewritten, fixed Python code — no prose."""
    client = _get_client()
    if client is None:
        return (
            "# GROQ_API_KEY not set — cannot generate improved code.\n"
            "# Local: add GROQ_API_KEY=<key> to your .env file.\n"
            "# Deploy: reflex deploy --env GROQ_API_KEY=<key>"
        )

    formatted_errors = "\n".join(
        f"- {e['type']}: {e.get('message', '')}" for e in detected_errors
    ) or "None."

    user_msg = (
        f"Detected issues:\n{formatted_errors}\n\n"
        f"Original code:\n{code}"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": _IMPROVE_SYSTEM},
                {"role": "user",   "content": user_msg},
            ],
            max_tokens=2048,
            temperature=0.1,
        )
        raw = (response.choices[0].message.content or "").strip()
        # Strip accidental markdown fences the model sometimes adds
        if raw.startswith("```"):
            lines = [ln for ln in raw.split("\n") if not ln.strip().startswith("```")]
            raw = "\n".join(lines).strip()
        return raw
    except Exception as e:
        print(f"[ai_suggester] Groq improve error: {e}")
        return f"# Could not generate improved code: {e}"