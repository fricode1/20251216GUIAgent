from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
import os, asyncio


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

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="You're a helpful assistant named Friday.",
        model=create_model(),
        memory=InMemoryMemory(),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
    )

    user = UserAgent(name="user")

    msg = None
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break

asyncio.run(main())