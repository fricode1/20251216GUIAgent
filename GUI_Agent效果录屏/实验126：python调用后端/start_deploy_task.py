import requests
import urllib3

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def start_deploy_task(
    task_id: str = "91",  # <--- 默认传入你需要启动的任务 ID
    authorization: str = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA",
    base_url: str = "https://62.168.243.10:19080"
):
    """
    启动布控应用的 API 封装函数
    """
    # 拼接完整的 URL
    url = f"{base_url}/mrag/api/deploy/tasks/start"
    
    # 设置请求头 Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    
    # 设置请求体 Body
    payload = {
        "id": task_id
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=payload, verify=False)
        
        # 检查 HTTP 状态码是否正常
        response.raise_for_status() 
        
        # 返回解析后的 JSON 字典
        return response.json()      
        
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        # 打印服务器返回的详细错误信息
        if hasattr(e, 'response') and e.response is not None:
            print(f"服务器返回报错内容: {e.response.text}")
        return None


# ==========================================
# 调用示例与结果解析
# ==========================================
if __name__ == "__main__":
    
    target_id = "91"
    print(f"正在请求服务器，尝试启动布控应用 (ID: {target_id})...\n")
    
    # 调用函数，这里 task_id 默认已经是 "91"，你可以随时改为其他 ID 比如 start_deploy_task(task_id="88")
    result = start_deploy_task(task_id=target_id)
    
    if result:
        # 判断业务状态码 code 是否为 0 (通常 0 代表成功)
        if result.get("code") == 0:
            print(f"✅ 启动成功！应用 (ID: {target_id}) 已开始运行。")
            print("服务器返回数据:", result)
        else:
            print(f"❌ 启动失败，服务器返回信息: {result.get('msg')}")
            print("完整返回内容:", result)