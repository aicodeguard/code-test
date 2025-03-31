import ast

class StyleRules:
    @staticmethod
    def check_naming_convention(node):
        violations = []
        if isinstance(node, ast.FunctionDef):
            if not node.name.islower():
                violations.append(f"函数命名不符合蛇形命名: {node.name}")
        return violations