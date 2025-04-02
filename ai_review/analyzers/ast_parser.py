import ast
from typing import List, Dict, Any

class ASTAnalyzer(ast.NodeVisitor):
    """AST分析器，用于检测代码质量问题"""
    
    def __init__(self):
        self.findings: List[str] = []
        self.function_complexity: Dict[str, int] = {}
        self.references: List[ast.Name] = []
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        分析函数定义，计算复杂度
        
        Args:
            node: 函数定义节点
        """
        # 计算圈复杂度
        complexity = len(node.body)
        # 计算函数复杂度
        complexity = self.calculate_function_complexity(node)
        # 计算函数复杂度
        self.function_complexity[node.name] = complexity
        self.generic_visit(node)

    def calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """
        计算函数的圈复杂度
        
        Args:
            node: 函数定义节点
        Returns:
            int: 函数的圈复杂度
        """
        complexity = 1  # 基础复杂度
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        return complexity

    def visit_Name(self, node: ast.Name) -> None:
        """
        检查变量使用情况
        
        Args:
            node: 变量节点
        """
        if isinstance(node.ctx, ast.Store):
            self._check_unused_variable(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        检查赋值语句
        
        Args:
            node: 赋值节点
        """
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(target.ctx, ast.Store):
                self._check_unused_variable(target)
        self.generic_visit(node)

    def _check_unused_variable(self, node: ast.Name) -> None:
        """
        检查变量是否未使用
        
        Args:
            node: 变量节点
        """
        if not any(ref.id == node.id for ref in self.references):
            self.findings.append(f"未使用变量: {node.id}")

    def visit_Assert(self, node: ast.Assert) -> ast.Any:
        return super().visit_Assert(node)