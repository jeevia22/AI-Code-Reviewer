import ast

def parse_code(code_string: str):
    """
    Parse Python code and check for syntax errors using AST.

    Args:
        code_string (str): Python code to analyze

    Returns:
        dict: Result with success status and details
    """

    
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {
            "success": False,
            "error": {
                "type": "SyntaxError",
                "message": str(e)
            }
        }

    
    formatted_code = ast.unparse(tree)

    
    ast_structure = ast.dump(tree, indent=4)

    return {
        "success": True,
        "formatted_code": formatted_code,
        "ast_dump": ast_structure
    }


if __name__ == "__main__":
    
    user_code = """
def calculate_sum(a,b):
 result = a+b
 if result > 10:
     print("Greater than 10")
 else:
     print("Less than or equal to 10")
 return result
"""

    result = parse_code(user_code)

    if not result["success"]:
        print(" Error found:")
        print(result["error"]["message"])
    else:
        print(" Code parsed successfully!\n")

        print(" Formatted Code ")
        print(result["formatted_code"])

        print("\n AST Dump ")
        print(result["ast_dump"])
