# app.py
from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from create_deploy_task import create_deploy_task
from list_deploy_alarms import list_deploy_alarms
from spider import pedestrian_violation
import requests
import urllib3

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
    # ... 省略了纯文本输出部分，因为前端需要 dict
    return simplified_list

# --- 初始化 AI Agent ---
api_key = "172423d8-0ab8-4e60-659b-de3cda928f95"
model_name = "qwen3-235b-a22b"
base_url = "http://44.71.1.34:8088/lm/v2/"

llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name
)

# 初始化 Agent
agent = create_agent(
    model=llm,
    tools=[create_deploy_task, list_deploy_alarms, pedestrian_violation],
    system_prompt="You are a helpful assistant",
)

# --- Flask Web 服务 ---
app = Flask(__name__)

@app.route('/')
def index():
    # 渲染前端页面
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    # 接收前端传来的历史消息上下文
    messages_history = data.get("messages", [])
    
    if not messages_history:
        return jsonify({"code": 400, "msg": "消息不能为空"})

    try:
        # 调用 LangChain Agent
        response = agent.invoke({"messages": messages_history})
        
        # 使用你的格式化函数，将结果转化为干净的字典列表返回给前端
        clean_msgs = simplify_langchain_messages(response, output_format="dict")
        
        return jsonify({
            "code": 200, 
            "data": clean_msgs
        })
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})

if __name__ == "__main__":
    # 在局域网所有网卡上运行，端口设为 5000
    app.run(host="0.0.0.0", port=5000, debug=True)