import ast

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.function_complexity = {}

    def visit_FunctionDef(self, node):
        # 计算圈复杂度
        complexity = len(node.body)
        # 计算函数复杂度
        complexity = self.calculate_function_complexity(node)
        # 计算函数复杂度
        self.function_complexity[node.name] = complexity
        self.generic_visit(node)

    def visit_Name(self, node):
        # 检测未使用变量
        if isinstance(node.ctx, ast.Store):
            if not any(ref.id == node.id for ref in self.references):
                self.findings.append(f"未使用变量: {node.id}")

    def visit_Assign(self, node):
        # 检测未使用变量
        if isinstance(node.targets[0].ctx, ast.Store):
            if not any(ref.id == node.targets[0].id for ref in self.references):
                self.findings.append(f"未使用变量: {node.targets[0].id}")
    
    def visit_Assert(self, node: ast.Assert) -> ast.Any:
        return super().visit_Assert(node)