# LABEL: BENIGN
# Calculator using eval() for expression parsing — legitimate use of eval
import re

def safe_eval(expression: str) -> float:
    """Evaluate a mathematical expression safely."""
    # Whitelist only numbers and operators
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
        raise ValueError(f"Invalid expression: {expression}")
    return eval(expression)  # safe: input validated above

if __name__ == "__main__":
    tests = ["2 + 2", "3 * (4 + 5)", "100 / 4", "2 ** 8"]
    for expr in tests:
        print(f"{expr} = {safe_eval(expr)}")
