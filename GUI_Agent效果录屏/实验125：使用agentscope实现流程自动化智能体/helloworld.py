from agentscope.agent import ReActAgent, AgentBase
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
import asyncio
import os

from agentscope.tool import Toolkit, execute_python_code

# DeepSeek 配置
api_key = "sk-588ceaf7b0f542f8881fb62161e9127c"
model_name = "deepseek-chat"
base_url = "https://api.deepseek.com"

def create_model():
    """创建通用模型配置"""
    return OpenAIChatModel(
        model_name=model_name,
        api_key=api_key,
        client_kwargs={"base_url": base_url},
    )


async def creating_react_agent() -> None:
    """创建一个 ReAct 智能体并运行一个简单任务。"""
    # 准备工具
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    jarvis = ReActAgent(
        name="Jarvis",
        sys_prompt="你是一个名为 Jarvis 的助手",
        model=create_model(),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    msg = Msg(
        name="user",
        content="你好！Jarvis，用 Python 运行 Hello World。",
        role="user",
    )

    await jarvis(msg)


asyncio.run(creating_react_agent())