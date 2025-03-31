import openai

class AICodeReviewer:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_optimization_suggestion(self, code_snippet):
        prompt = f"请对以下Python代码进行审查:\n{code_snippet}\n建议："
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()