import openai
from configparser import ConfigParser

class AIModelHandler:
    def __init__(self, config_path='model_config.yaml'):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path):
        with open(path) as f:
            return yaml.safe_load(f)

    def get_code_review(self, code_snippet: str, context: dict) -> str:
        """调用AI模型进行语义级审查"""
        prompt = f"""作为资深Python架构师，请审查以下代码：
{code_snippet}
审查重点：
1. 架构设计合理性
2. 异常处理完整性
3. 性能优化空间
4. 安全合规性
请用中文按严重性分级输出建议"""
        
        response = openai.ChatCompletion.create(
            model=self.config['openai']['model_name'],
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config['openai']['temperature']
        )
        return response.choices[0].message.content