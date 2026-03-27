from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


def simplify_langchain_messages(data, output_format="text"):
    """
    简化 LangChain 消息输出
    :param data: 包含 'messages' 列表的字典，或直接是 messages 列表
    :param output_format: "text" (返回格式化字符串) 或 "dict" (返回干净的字典列表)
    """
    # 兼容传入整体 dict 或直接传入 list 的情况
    messages = data.get('messages', data) if isinstance(data, dict) else data
    
    simplified_list = []

    for msg in messages:
        # 获取对象的类名（例如 'HumanMessage', 'AIMessage' 等）
        msg_type = type(msg).__name__
        
        # 如果是字典（比如经过了 model_dump），则直接取值；如果是对象，则用 getattr
        content = getattr(msg, 'content', '') if not isinstance(msg, dict) else msg.get('content', '')
        
        clean_msg = {"role": "", "content": content}

        # 1. 处理人类消息
        if msg_type == 'HumanMessage':
            clean_msg["role"] = "👤 User"
            
        # 2. 处理 AI 消息
        elif msg_type == 'AIMessage':
            clean_msg["role"] = "🤖 AI"
            # 提取工具调用信息 (如果有)
            tool_calls = getattr(msg, 'tool_calls', []) if not isinstance(msg, dict) else msg.get('tool_calls', [])
            if tool_calls:
                calls_str = ", ".join([f"{tc.get('name')}({tc.get('args')})" for tc in tool_calls])
                clean_msg["tool_calls"] = calls_str
                
        # 3. 处理工具返回消息
        elif msg_type == 'ToolMessage':
            tool_name = getattr(msg, 'name', 'Unknown') if not isinstance(msg, dict) else msg.get('name', 'Unknown')
            clean_msg["role"] = f"🛠️ Tool [{tool_name}]"

        simplified_list.append(clean_msg)

    # ==== 根据需要的格式返回 ====
    if output_format == "dict":
        return simplified_list
    
    # 格式化为易读的文本
    text_output = []
    for item in simplified_list:
        text = f"{item['role']}:\n{item['content']}"
        if "tool_calls" in item:
            text += f"\n(🔧 触发工具: {item['tool_calls']})"
        text_output.append(text)
        
    return "\n" + "-"*40 + "\n".join(text_output) + "\n" + "-"*40


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

print(simplify_langchain_messages(response))
