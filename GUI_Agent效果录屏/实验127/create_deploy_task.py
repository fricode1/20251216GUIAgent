import requests
import urllib3

# 导入提取地点和地点转摄像头的函数 (请确保这三个py文件在同一个目录下)
from language_to_location import language_to_location
from location_to_camera import location_to_camera

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_deploy_task(user_input: str):
    """
    根据用户输入的自然语言，自动提取地点、转换为摄像头ID，并创建布控任务
    """
    print(f"1. 收到用户输入: '{user_input}'")
    
    # ---------------------------------------------------------
    # 第一步：从自然语言中提取地点
    # ---------------------------------------------------------
    location = language_to_location(user_input)
    if not location or location == "无":
        print("❌ 错误: 无法从输入中提取到有效的地理位置信息，任务创建终止。")
        return None
    print(f"✅ 成功提取地点: {location}")

    # ---------------------------------------------------------
    # 第二步：将地点转换成相机ID (apeId)
    # ---------------------------------------------------------
    camera_id = location_to_camera(location)
    if not camera_id:
        print(f"❌ 错误: 未能在系统中查找到地点 '{location}' 对应的摄像头，任务创建终止。")
        return None
    print(f"✅ 成功获取摄像头ID: {camera_id}")

    # ---------------------------------------------------------
    # 第三步：组装请求并创建布控任务
    # ---------------------------------------------------------
    # 预设的环境及认证参数 (均来自原文件默认值)
    base_url = "https://62.168.243.10:19080"
    authorization = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImVhMjlkZWQ2LTIxODgtNDM1Mi1hY2IwLTJkNjYzMDQ1ZDY5YSJ9.zB3zVMF_myi729dV_1PfZn9hgBWTzmWAsGyJ2ata17q-HKtsnC67c_28VJKiuExpnhVBKj-DvnmqvaOSJPEaiQ"
    
    url = f"{base_url}/mrag/api/deploy/tasks/create"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    
    # 使用获取到的动态 camera_id 组装时空列表
    space_time_list = [
        {
            "device_id": camera_id,
            "start_time": "2026-03-17 00:00:00",
            "end_time": "2026-03-24 23:59:59",
            "time_slot_list": []
        }
    ]
    
    # 组装请求体 Body
    payload = {
        "name": "test1",
        "deploy_type": 0,
        "left_seconds": 0,
        "right_seconds": 0,
        "target_type": "person",
        "desc": "test2",
        "text": user_input,       # 将用户的完整描述作为文本检索条件
        "image_base64": "",
        "space_time_list": space_time_list,
        "distance": 0.8,
        "prompt": "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
        "prompt_image_base64_list": [],
        "isrealtime": 0
    }

    try:
        print("3. 正在向服务器发送创建布控请求...")
        # 发送 POST 请求，verify=False 用于跳过 HTTPS(IP) 证书校验
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status() 
        return response.json()      
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求发生异常: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"服务器返回报错内容: {e.response.text}")
        return None


# ==========================================
# 极简调用示例：
# ==========================================
if __name__ == "__main__":
    # 你只需传入用户讲的一句话即可
    user_query = "查询新华路穿白衣服的人"
    
    print("=" * 40)
    result = create_deploy_task(user_query)
    
    if result:
        print("=" * 40)
        print("🎉 任务创建成功，服务器返回数据：")
        print(result)