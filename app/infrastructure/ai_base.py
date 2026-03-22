from abc import ABC, abstractmethod

class AIBase(ABC):
    @abstractmethod
    async def chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        """
        发送对话请求到大模型并返回原始字符串
        :param system_prompt: 系统指令，定义 AI 角色和行为
        :param user_prompt: 用户输入的原始菜谱内容
        :return: AI 返回的 JSON 字符串
        """
        pass