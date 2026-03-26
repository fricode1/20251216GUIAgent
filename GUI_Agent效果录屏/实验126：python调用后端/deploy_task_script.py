import requests
import urllib3
import time
from typing import List, Dict, Any

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =====================================================================
# 基础配置 (供所有函数使用默认值)
# =====================================================================
DEFAULT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA"
DEFAULT_BASE_URL = "https://62.168.243.10:19080"

# =====================================================================
# 函数 1：创建布控应用
# =====================================================================
def create_deploy_task(
    name: str = "test1",
    authorization: str = DEFAULT_TOKEN,
    target_type: str = "person",
    desc: str = "test2",
    deploy_type: int = 0,
    image_base64: str = "",
    text: str = "穿白衣服的人",
    distance: float = 0.8,
    prompt: str = "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
    space_time_list: List[Dict[str, Any]] = None,
    prompt_image_base64_list: List[str] = None,
    left_seconds: int = 0,
    right_seconds: int = 0,
    isrealtime: int = 0,
    base_url: str = DEFAULT_BASE_URL
):
    if space_time_list is None:
        space_time_list = [{
            "device_id": "41132867111327248002",
            "start_time": "2026-03-17 00:00:00",
            "end_time": "2026-03-24 23:59:59",
            "time_slot_list": []
        }]
    if prompt_image_base64_list is None:
        prompt_image_base64_list = []

    url = f"{base_url}/mrag/api/deploy/tasks/create"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    payload = {
        "name": name, "deploy_type": deploy_type, "left_seconds": left_seconds,
        "right_seconds": right_seconds, "target_type": target_type, "desc": desc,
        "text": text, "image_base64": image_base64, "space_time_list": space_time_list,
        "distance": distance, "prompt": prompt, 
        "prompt_image_base64_list": prompt_image_base64_list, "isrealtime": isrealtime
    }
    
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response.raise_for_status() 
    return response.json()

# =====================================================================
# 函数 2：获取所有布控应用
# =====================================================================
def list_deploy_tasks(
    authorization: str = DEFAULT_TOKEN,
    base_url: str = DEFAULT_BASE_URL
):
    url = f"{base_url}/mrag/api/deploy/tasks/list"
    headers = {"Authorization": authorization}
    
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status() 
    return response.json()

# =====================================================================
# 函数 3：启动布控应用
# =====================================================================
def start_deploy_task(
    task_id: str,
    authorization: str = DEFAULT_TOKEN,
    base_url: str = DEFAULT_BASE_URL
):
    url = f"{base_url}/mrag/api/deploy/tasks/start"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    payload = {"id": str(task_id)}
    
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response.raise_for_status() 
    return response.json()

# =====================================================================
# 函数 4：查看布控结果（告警列表）
# =====================================================================
def list_deploy_alarms(
    task_id: str,
    page_no: int = 1,
    page_size: int = 10,
    authorization: str = DEFAULT_TOKEN,
    base_url: str = DEFAULT_BASE_URL
):
    url = f"{base_url}/mrag/api/deploy/alarm/list"
    headers = {"Authorization": authorization}
    params = {"id": str(task_id), "pageNo": page_no, "pageSize": page_size}
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    response.raise_for_status() 
    return response.json()


# =====================================================================
# 主业务流程：串联以上4个函数
# =====================================================================
if __name__ == "__main__":
    
    # 动态生成一个带时间戳的任务名，防止重名报错
    task_name = f"auto_task_{int(time.time())}"
    
    # ---------------------------------------------------------
    # 步骤 1：创建应用
    # ---------------------------------------------------------
    print(f"🔄 [1/4] 正在创建布控应用: {task_name}...")
    create_res = create_deploy_task(name=task_name)
    
    if create_res is None or create_res.get("code") != 0:
        print(f"❌ 创建失败，退出。返回信息: {create_res}")
        exit(1)
    
    print("✅ 创建请求发送成功！")

    # ---------------------------------------------------------
    # 步骤 2：获取应用 ID
    # ---------------------------------------------------------
    print("🔄 [2/4] 正在获取刚创建的应用 ID...")
    task_id = None
    
    # 调用函数2：获取任务列表
    list_res = list_deploy_tasks()
    if list_res and list_res.get("code") == 0:
        # 遍历列表，找到刚才创建的那个 task_name，取出它的 id
        task_list = list_res.get("data", {}).get("list", [])
        for task in task_list:
            if task.get("name") == task_name:
                task_id = str(task.get("id"))
                break
                
    if not task_id:
        print("❌ 未能在列表中找到刚才创建的任务，退出。")
        exit(1)
        
    print(f"✅ 成功提取到任务 ID: {task_id}")

    # ---------------------------------------------------------
    # 步骤 3：启动该应用
    # ---------------------------------------------------------
    print(f"🔄 [3/4] 正在启动应用 (ID: {task_id})...")
    # 调用函数3：启动任务
    start_res = start_deploy_task(task_id=task_id)
    
    if start_res is None or start_res.get("code") != 0:
        print(f"❌ 启动失败，退出。返回信息: {start_res}")
        exit(1)
        
    print("✅ 应用启动成功！")

    # ---------------------------------------------------------
    # 步骤 4：轮询并打印告警
    # ---------------------------------------------------------
    print("\n🔄 [4/4] 开始监听告警 (按 Ctrl+C 停止监听)...\n")
    
    # 用于记录已经处理过的告警 ID，避免重复打印
    seen_alarm_ids = set()
    
    try:
        while True:
            # 调用函数4：获取告警列表（取前10条）
            alarm_res = list_deploy_alarms(task_id=task_id, page_no=1, page_size=10)
            
            if alarm_res and alarm_res.get("code") == 0:
                alarms = alarm_res.get("data", {}).get("list", [])
                
                # 倒序遍历（让最旧的先打，最新的后打，符合时间直觉）
                for alarm in reversed(alarms):
                    a_id = str(alarm.get("id"))
                    
                    # 发现新的告警（ID 不在我们的已读集合中）
                    if a_id not in seen_alarm_ids:
                        seen_alarm_ids.add(a_id)
                        
                        a_time = alarm.get("time")
                        a_sim = alarm.get("similar")
                        a_url = alarm.get("url")
                        
                        print(f"🚨 [新告警] ID: {a_id:<8} | 时间: {a_time} | 相似度: {a_sim:<6.4f} | 图片: {a_url}")
            
            # 休眠 5 秒后再次轮询，避免对服务器造成极大压力
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 监听已手动终止。")