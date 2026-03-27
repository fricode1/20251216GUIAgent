from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


llm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # 关键点：替换为本地地址
    api_key="sk-588ceaf7b0f542f8881fb62161e9127c",                    # 关键点：本地部署通常不需要真实 Key
    model="deepseek-chat"                       # 关键点：指定你本地运行的模型名称
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_coord(city):
    """get gps coord for a given city"""
    return f"The gps coord of {city} is [123, 456]"

agent = create_agent(
    model=llm,
    tools=[get_weather, get_coord],
    system_prompt="You are a helpful assistant",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in 北京？What is the gps coord of sf？"}]}
)

print(response)
