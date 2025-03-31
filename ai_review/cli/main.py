from analyzers.ast_parser import ASTAnalyzer
from rules import style, security

def code_review(file_path):
    # AST解析
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    # 执行静态分析
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)
    
    # 应用规则检查
    style_violations = StyleRules.check_naming_convention(tree)
    security_issues = SecurityRules.check_injection(tree)
    
    # AI增强审查
    if config['ai']['enable']:
        ai_reviewer = AICodeReviewer(config['ai']['api_key'])
        ai_suggestions = ai_reviewer.get_optimization_suggestion(code_snippet)
    
    # 生成报告
    generate_report({
        'static_analysis': analyzer.findings,
        'style_violations': style_violations,
        'ai_suggestions': ai_suggestions
    })
# import click
# from ai_review.core.analyzer import CodeAnalyzer
# from ai_review.core.model_adapter import AIModelHandler

# @click.command()
# @click.argument('file_path')
# @click.option('--ai', is_flag=True, help='启用AI增强审查')
# def review(file_path: str, ai: bool):
#     """执行代码审查流水线"""
#     with open(file_path) as f:
#         code = f.read()
    
#     # 静态规则审查
#     analyzer = CodeAnalyzer(['ai_review.rules.security_rules'])
#     findings = analyzer.analyze(code)
    
#     # AI增强分析
#     if ai:
#         ai_handler = AIModelHandler()
#         ai_comment = ai_handler.get_code_review(code, {'findings': findings})
#         print(ai_comment)
#         print(type(ai_comment))
#         print(ai_comment.keys())
#         click.echo(f"\nAI审查建议:\n{ai_comment}")
    
#     # 输出格式化结果
#     click.echo("\n静态审查结果:")
#     for issue in findings:
#         click.secho(f"[{issue['severity'].upper()}] Line {issue['line']}: {issue['message']}", 
#                    fg='red' if issue['severity'] == 'critical' else 'yellow')