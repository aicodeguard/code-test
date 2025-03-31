import ast

def detect_unsafe_functions(tree) -> list:
    """识别高危函数调用"""
    unsafe_calls = {
        'eval', 'exec', 'pickle.loads', 'pickle.load',
        'subprocess.call', 'subprocess.Popen', 'os.system',
        'tempfile.mktemp'  # Use mkstemp instead
    }
    return [{
        'msg': f"检测到不安全函数调用: {node.func.id}",
        'level': 'critical',
        'lineno': node.lineno
    } for node in ast.walk(tree) 
     if isinstance(node, ast.Call) 
     and hasattr(node.func, 'id') 
     and node.func.id in unsafe_calls]

def check_hardcoded_secrets(tree) -> list:
    """检测硬编码密钥"""
    secret_patterns = {'password', 'secret_key', 'api_key'}
    return [{
        'msg': f"疑似硬编码凭证: {node.targets[0].id}",
        'level': 'high',
        'lineno': node.lineno
    } for node in ast.walk(tree) 
     if isinstance(node, ast.Assign)
     and any(pattern in node.targets[0].id.lower() for pattern in secret_patterns)]