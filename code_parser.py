import ast


def parse_code(code_string: str):
    """
    Parse Python code and check for syntax errors.

    Args:
        code_string (str): Python code to analyze

    Returns:
        dict: Result containing parsing status and details
    """

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

    # If syntax is correct
    formatted_code = ast.unparse(tree)
    ast_structure = ast.dump(tree, indent=4)

    return {
        "success": True,
        "formatted_code": formatted_code,
        "ast_dump": ast_structure
    }


# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":

    test_code = """
def calculate_sum(a, b):
    result = a + b
    if result > 10:
        print("Greater than 10")
    else:
        print("Less than or equal to 10")
    return result

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, " + self.name)

for i in range(5)
    print(i)
"""

    result = parse_code(test_code)

    print(result)