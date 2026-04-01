# app.py
from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage # 新增导入
from create_deploy_task import create_deploy_task
from list_deploy_tasks import list_deploy_tasks
from list_deploy_alarms import list_deploy_alarms
from spider import pedestrian_violation
import config
import urllib3
import uuid # 新增导入

# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 你的原生辅助函数 ---
def simplify_langchain_messages(data, output_format="text"):
    messages = data.get('messages', data) if isinstance(data, dict) else data
    simplified_list = []
    for msg in messages:
        msg_type = type(msg).__name__
        content = getattr(msg, 'content', '') if not isinstance(msg, dict) else msg.get('content', '')
        clean_msg = {"role": "", "content": content}

        if msg_type == 'HumanMessage' or (isinstance(msg, dict) and msg.get("role") == "user"):
            clean_msg["role"] = "user"
            clean_msg["display_role"] = "👤 User"
        elif msg_type == 'AIMessage' or (isinstance(msg, dict) and msg.get("role") == "assistant"):
            clean_msg["role"] = "assistant"
            clean_msg["display_role"] = "🤖 AI"
            tool_calls = getattr(msg, 'tool_calls', []) if not isinstance(msg, dict) else msg.get('tool_calls', [])
            if tool_calls:
                calls_str = ", ".join([f"{tc.get('name')}({tc.get('args')})" for tc in tool_calls])
                clean_msg["tool_calls"] = calls_str
        elif msg_type == 'ToolMessage' or (isinstance(msg, dict) and msg.get("role") == "tool"):
            tool_name = getattr(msg, 'name', 'Unknown') if not isinstance(msg, dict) else msg.get('name', 'Unknown')
            clean_msg["role"] = "tool"
            clean_msg["display_role"] = f"🛠️ Tool [{tool_name}]"
        
        simplified_list.append(clean_msg)

    if output_format == "dict":
        return simplified_list
    return simplified_list

# --- 初始化 AI Agent ---
model_name = "qwen3-235b-a22b"
base_url = "http://44.71.1.34:8088/lm/v2/"

llm = ChatOpenAI(
    base_url=base_url,
    api_key=config.api_key,
    model=model_name
)

# 初始化 Agent
agent = create_agent(
    model=llm,
    tools=[create_deploy_task, list_deploy_tasks, list_deploy_alarms, pedestrian_violation],
    system_prompt="You are a helpful assistant",
)

# --- Flask Web 服务 ---
app = Flask(__name__)

# --- 新增：用于在内存中存储会话历史的字典 ---
session_store = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    print('调用chat接口')
    data = request.json
    
    # 获取前端传来的会话ID和最新消息
    session_id = data.get("session_id")
    user_message = data.get("message")
    
    if not user_message or not session_id:
        return jsonify({"code": 400, "msg": "消息或会话ID不能为空"})

    # 初始化或获取当前会话的历史记录
    if session_id not in session_store:
        session_store[session_id] = []
        
    try:
        # 将用户最新的一句话追加到后端的历史记录中（保留 LangChain 原生对象）
        session_store[session_id].append(HumanMessage(content=user_message))
        
        print('启动智能体')
        # 将完整的、包含所有原生对象的历史记录传给 Agent
        response = agent.invoke({"messages": session_store[session_id]})
        
        # 关键步骤：更新后端的历史记录为 Agent 返回的完整记录 
        # (这包含了带有正确 tool_call_id 的 AIMessage 和 ToolMessage)
        session_store[session_id] = response["messages"]
        
        # 使用你的格式化函数，提取显示所需内容返回给前端渲染
        clean_msgs = simplify_langchain_messages(response, output_format="dict")
        
        return jsonify({
            "code": 200, 
            "data": clean_msgs
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"code": 500, "msg": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)