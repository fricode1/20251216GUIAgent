from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from create_deploy_task import create_deploy_task
from list_deploy_alarms import list_deploy_alarms
from spider import pedestrian_violation
import requests
import urllib3

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_deploy_tasks(
    authorization: str = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImVhMjlkZWQ2LTIxODgtNDM1Mi1hY2IwLTJkNjYzMDQ1ZDY5YSJ9.zB3zVMF_myi729dV_1PfZn9hgBWTzmWAsGyJ2ata17q-HKtsnC67c_28VJKiuExpnhVBKj-DvnmqvaOSJPEaiQ",
    base_url: str = "https://62.168.243.10:19080"
):
    """列出所有布控应用"""
    return_str = ''
    url = f"{base_url}/mrag/api/deploy/tasks/list"
    headers = {
        "Authorization": authorization
    }
    # 发送 GET 请求
    response = requests.get(url, headers=headers, verify=False)
    try:
        response.raise_for_status()
        result = response.json()

        if result:
            # 判断业务状态码 code 是否为 0 (通常 0 代表成功)
            if result.get("code") == 0:
                data = result.get("data", {})
                total = data.get("total", 0)
                task_list = data.get("list", [])

                # 遍历并打印精简后的任务列表信息，方便查看
                for task in task_list:
                    task_id = task.get('id', 'N/A')
                    task_name = task.get('name', 'N/A')
                    status_code = task.get('status', 0)
                    status_str = "运行中" if status_code == 1 else "已停止"
                    return_str += '任务ID：{}，任务状态：{}，任务名称：{}。\n'.format(task_id, status_str, task_name)
            else:
                return_str += f"❌ 获取失败，服务器返回信息: {result.get('msg')}"
    except Exception as e:
        return_str += e
    return  return_str


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

    return "\n" + "-" * 40 + "\n".join(text_output) + "\n" + "-" * 40


def main():
    api_key = "172423d8-0ab8-4e60-659b-de3cda928f95"
    model_name = "qwen3-235b-a22b"
    base_url = "http://44.71.1.34:8088/lm/v2/"

    llm = ChatOpenAI(
        base_url=base_url,  # 关键点：替换为本地地址
        api_key=api_key,  # 关键点：本地部署通常不需要真实 Key
        model=model_name  # 关键点：指定你本地运行的模型名称
    )
    agent = create_agent(
        model=llm,
        tools=[create_deploy_task, list_deploy_alarms, pedestrian_violation],
        system_prompt="You are a helpful assistant",
    )
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "创建行人违章查询应用"}]}
    )
    print(simplify_langchain_messages(response))


if __name__ == "__main__":
    main()