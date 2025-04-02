from threading import Lock

from jinja2 import Environment, StrictUndefined
from tiktoken import encoding_for_model, get_encoding

from ai_review.config_loader import get_settings
from ai_review.log import get_logger


class TokenEncoder:
    _encoder_instance = None
    _model = None
    _lock = Lock()  # Create a lock object

    @classmethod
    def get_token_encoder(cls):
        model = get_settings().config.model
        if cls._encoder_instance is None or model != cls._model:  # Check without acquiring the lock for performance
            with cls._lock:  # Lock acquisition to ensure thread safety
                if cls._encoder_instance is None or model != cls._model:
                    cls._model = model
                    cls._encoder_instance = encoding_for_model(cls._model) if "gpt" in cls._model else get_encoding(
                        "cl100k_base")
        return cls._encoder_instance


class TokenHandler:
    """
    A class for handling tokens in the context of a pull request.

    Attributes:
    - encoder: An object of the encoding_for_model class from the tiktoken module. Used to encode strings and count the
      number of tokens in them.
    - limit: The maximum number of tokens allowed for the given model, as defined in the MAX_TOKENS dictionary in the
      pr_agent.algo module.
    - prompt_tokens: The number of tokens in the system and user strings, as calculated by the _get_system_user_tokens
      method.
    """

    def __init__(self, pr=None, vars: dict = None, system: str = "", user: str = ""):
        """
        初始化 TokenHandler 对象
        
        Args:
            pr: Pull Request 对象
            vars: 变量字典，默认为空字典
            system: 系统提示字符串
            user: 用户提示字符串
        """
        self.vars = vars or {}  # 使用更简洁的空字典初始化
        self.encoder = TokenEncoder.get_token_encoder()
        self.prompt_tokens = (self._get_system_user_tokens(pr, self.encoder, self.vars, system, user) 
                            if pr is not None else 0)

    def _get_system_user_tokens(self, pr, encoder, vars: dict, system: str, user: str) -> int:
        """
        计算系统和用户字符串中的令牌数
        
        Args:
            pr: Pull Request 对象
            encoder: tiktoken 编码器实例
            vars: 变量字典
            system: 系统提示字符串
            user: 用户提示字符串
            
        Returns:
            int: 系统和用户字符串中的总令牌数
        """
        try:
            environment = Environment(undefined=StrictUndefined)
            system_prompt = environment.from_string(system).render(vars)
            user_prompt = environment.from_string(user).render(vars)
            
            return len(encoder.encode(system_prompt)) + len(encoder.encode(user_prompt))
            
        except Exception as e:
            get_logger().error(f"Error in _get_system_user_tokens: {str(e)}")
            return 0

    def count_tokens(self, patch: str) -> int:
        """
        计算给定补丁字符串中的令牌数
        
        Args:
            patch: 补丁字符串
            
        Returns:
            int: 补丁字符串中的令牌数
        """
        return len(self.encoder.encode(patch, disallowed_special=()))
