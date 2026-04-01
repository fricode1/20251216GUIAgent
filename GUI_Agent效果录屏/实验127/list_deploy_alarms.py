import requests
import urllib3
import config

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_deploy_alarms(
    task_id: str = "21"
):
    """
    列出指定任务的告警信息
    """
    # 接口的基础路径（不包含查询参数）
    base_url = "https://62.168.243.10:19080"
    url = f"{base_url}/mrag/api/deploy/alarm/list"
    
    # 设置请求头 Headers
    headers = {
        "Authorization": config.authorization
    }
    
    # 设置 URL 查询参数 (Query Parameters)
    params = {
        "id": task_id,
        "pageNo": 1,
        "pageSize": 10
    }

    try:
        # 发送 GET 请求，把 params 传给 requests 即可自动拼接到 URL 后面
        response = requests.get(url, headers=headers, params=params, verify=False)
        
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
    
    # 假设你想看第1页，每页10条的数据
    target_id = "21"
    print(f"正在获取布控应用 (ID: {target_id}) 的告警结果...\n")
    
    result = list_deploy_alarms(task_id=target_id)
    
    if result:
        if result.get("code") == 0:
            data = result.get("data", {})
            total = data.get("total", 0)
            alarm_list = data.get("list", [])
            
            print(f"✅ 获取成功！该任务共产生 {total} 条告警记录（当前显示第 1 页）。\n")
            
            # 打印表头
            print(f"{'告警ID':<8} | {'告警时间':<20} | {'相似度':<8} | {'目标类型':<8} | {'抓拍图片链接'}")
            print("-" * 100)
            
            # 遍历打印每一条告警信息
            for alarm in alarm_list:
                alarm_id = alarm.get('id', 'N/A')
                alarm_time = alarm.get('time', 'N/A')
                similar = alarm.get('similar', 0.0)
                target_type = alarm.get('type', 'N/A')
                image_url = alarm.get('url', 'N/A')
                
                # 格式化打印
                print(f"{alarm_id:<8} | {alarm_time:<20} | {similar:<8.4f} | {target_type:<8} | {image_url}")
                
            print("-" * 100)
            
        else:
            print(f"❌ 获取失败，服务器返回信息: {result.get('msg')}")
            print("完整返回内容:", result)