import ast


def parse_code(code_string: str) -> dict:
    """
    Parse Python using CPython's own AST module.

    This IS the real Python compiler front-end.
    SyntaxError type, message, line number, and column offset are
    identical to what the interpreter itself would report.
    """
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {
            "success": False,
            "error": {
                "type": "SyntaxError",
                "message": e.msg,           # clean message, no file/lineno noise
                "lineno": e.lineno,         # key is "lineno" — matches state.py
                "col_offset": e.offset,
            },
        }

    return {
        "success": True,
        "formatted_code": ast.unparse(tree),
    }