import ast


def parse_code(code_string: str):
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {
            "success": False,
            "error": {
                "type": "Syntax Error",
                "message": str(e),
                "line": e.lineno
            }
        }

    formatted_code = ast.unparse(tree)

    return {
        "success": True,
        "formatted_code": formatted_code
    }