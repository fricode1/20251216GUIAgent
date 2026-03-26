import requests
import urllib3

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_deploy_tasks(
    authorization: str = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA",
    base_url: str = "https://62.168.243.10:19080"
):
    """
    获取所有布控应用的 API 封装函数
    """
    # 拼接完整的 URL
    url = f"{base_url}/mrag/api/deploy/tasks/list"
    
    # 设置请求头 Headers
    headers = {
        "Authorization": authorization
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, headers=headers, verify=False)
        
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
    print("正在请求服务器获取布控应用列表...\n")
    
    # 直接调用，使用默认参数
    result = list_deploy_tasks()
    
    if result:
        # 判断业务状态码 code 是否为 0 (通常 0 代表成功)
        if result.get("code") == 0:
            data = result.get("data", {})
            total = data.get("total", 0)
            task_list = data.get("list", [])
            
            print(f"✅ 获取成功！当前系统中共找到 {total} 个布控应用。\n")
            print(f"{'任务ID':<6} | {'运行状态':<6} | {'任务名称'}")
            print("-" * 50)
            
            # 遍历并打印精简后的任务列表信息，方便查看
            for task in task_list:
                task_id = task.get('id', 'N/A')
                task_name = task.get('name', 'N/A')
                status_code = task.get('status', 0)
                status_str = "🟢 运行中" if status_code == 1 else "🔴 已停止"
                
                print(f"{task_id:<6} | {status_str:<6} | {task_name}")
                
            print("-" * 50)
            
            # 如果你想查看完整的原始 JSON 结构，取消下面这行的注释即可
            # print("\n原始返回数据:", result)
            
        else:
            print(f"❌ 获取失败，服务器返回信息: {result.get('msg')}")
            print("完整返回内容:", result)