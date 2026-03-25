import asyncio
import os
from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import OpenAIChatModel

# DeepSeek 配置
api_key = "sk-588ceaf7b0f542f8881fb62161e9127c"
model_name = "deepseek-chat"
base_url = "https://api.deepseek.com"

async def main():
    agent = ReActAgent(
        name="助手",
        sys_prompt="你是一个乐于助人的助手",
        model=OpenAIChatModel(
            model_name=model_name,
            api_key=api_key,
            client_kwargs={"base_url": base_url},
        ),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
    )
    
    # 运行智能体
    msg = Msg(name="user", content="你好！请自我介绍", role="user")
    await agent(msg)

asyncio.run(main())
