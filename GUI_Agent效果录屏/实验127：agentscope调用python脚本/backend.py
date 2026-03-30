"""
FastAPI 后端服务 - 调用 LangChain Agent
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# 初始化 LLM
llm = ChatOpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-588ceaf7b0f542f8881fb62161e9127c",
    model="deepseek-chat"
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_coord(city):
    """get gps coord for a given city"""
    return f"The gps coord of {city} is [123, 456]"

# 创建 agent
agent = create_agent(
    model=llm,
    tools=[get_weather, get_coord],
    system_prompt="You are a helpful assistant",
)

app = FastAPI(title="LangChain Agent API")

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class Message(BaseModel):
    role: str
    content: str
    tool_calls: list = []

class ChatResponse(BaseModel):
    messages: list[Message]

def simplify_messages(data):
    """简化 LangChain 消息输出"""
    messages = data.get('messages', data) if isinstance(data, dict) else data
    result = []

    for msg in messages:
        msg_type = type(msg).__name__
        content = getattr(msg, 'content', '') if not isinstance(msg, dict) else msg.get('content', '')

        clean_msg = {"role": "", "content": content, "tool_calls": []}

        if msg_type == 'HumanMessage':
            clean_msg["role"] = "user"
        elif msg_type == 'AIMessage':
            clean_msg["role"] = "assistant"
            tool_calls = getattr(msg, 'tool_calls', []) if not isinstance(msg, dict) else msg.get('tool_calls', [])
            if tool_calls:
                calls_str = ", ".join([f"{tc.get('name')}({tc.get('args')})" for tc in tool_calls])
                clean_msg["tool_calls"] = [{"name": tc.get('name'), "args": str(tc.get('args'))} for tc in tool_calls]
        elif msg_type == 'ToolMessage':
            tool_name = getattr(msg, 'name', 'Unknown') if not isinstance(msg, dict) else msg.get('name', 'Unknown')
            clean_msg["role"] = f"tool_{tool_name}"

        result.append(clean_msg)

    return result

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    response = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]}
    )

    messages = simplify_messages(response)

    return ChatResponse(messages=messages)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
