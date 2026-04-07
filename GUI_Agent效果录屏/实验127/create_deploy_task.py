import requests
import urllib3
import config

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_deploy_task(text_description, camera_ids):
    """
    根据 text_description 和 摄像头ID，创建布控任务
    input:
        text_description: 对要布控的对象的文本描述
        camera_ids: 多个相机的id，不同id间用英文逗号隔开，如'123,456'
    """
    camera_id_list = camera_ids.split(',')
    base_url = "https://62.168.243.10:19080"
    authorization = config.authorization
    
    url = f"{base_url}/mrag/api/deploy/tasks/create"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    
    # 使用获取到的动态 camera_id 组装时空列表
    space_time_list = []
    for camera_id_ in camera_id_list:
        space_time_dict = {
            "device_id": camera_id_,
            "start_time": "2026-03-17 00:00:00",
            "end_time": "2026-03-24 23:59:59",
            "time_slot_list": []
        }
        space_time_list.append(space_time_dict)
    print(space_time_list)

    # 组装请求体 Body
    payload = {
        "name": text_description,
        "deploy_type": 0,
        "left_seconds": 0,
        "right_seconds": 0,
        "target_type": "person",
        "desc": text_description,
        "text": text_description,       # 将用户的完整描述作为文本检索条件
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


if __name__ == '__main__':
    create_deploy_task(text_description='渣土车', camera_ids='41138130001312152683,41138131001312870011')