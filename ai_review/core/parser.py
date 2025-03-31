import ast
import astunparse

class ASTParser:
    def __init__(self, source_code: str):
        self.raw_code = source_code
        try:
            self.tree = ast.parse(source_code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax at line {e.lineno}: {e.msg}")
    def get_function_defs(self) -> list:
        """提取所有函数定义元数据"""
        return [{
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'lineno': node.lineno,
            'docstring': ast.get_docstring(node)
        } for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]

    def get_class_hierarchy(self) -> list:
        """解析类继承结构"""
        return [{
            'name': node.name,
            'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
            'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        } for node in ast.walk(self.tree) if isinstance(node, ast.ClassDef)]

    def code_visualization(self) -> str:
        """生成AST可视化结构"""
        return astunparse.dump(self.tree)