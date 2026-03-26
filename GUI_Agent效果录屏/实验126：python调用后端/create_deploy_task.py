import requests
import urllib3
from typing import List, Dict, Any

# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_deploy_task(
    # --- 必填项/核心设置赋予了你提供的默认值 ---
    authorization: str = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA",
    name: str = "test1",
    target_type: str = "person",
    desc: str = "test2",
    deploy_type: int = 0,
    image_base64: str = "",
    text: str = "穿白衣服的人",
    distance: float = 0.8,
    prompt: str = "描述:\n如果目标图片符合描述及示例图片，返回 Y，如果不是则返回 N。不要包含其他字符。\n上传的最后一张图片为目标图片。其他图片为目标示例图片。",
    
    # --- 列表类型默认传 None，在函数内初始化 ---
    space_time_list: List[Dict[str, Any]] = None,
    prompt_image_base64_list: List[str] = None,
    
    # --- 原接口中有但你刚才没提到的补充参数，保留默认值 0 ---
    left_seconds: int = 0,
    right_seconds: int = 0,
    isrealtime: int = 0,
    
    # --- 基础 URL ---
    base_url: str = "https://62.168.243.10:19080"
):
    """
    创建部署任务的 API 封装函数
    """
    
    # 1. 处理默认的可变类型参数 (list/dict)
    if space_time_list is None:
        space_time_list = [
            {
                "device_id": "41132867111327248002",
                "start_time": "2026-03-17 00:00:00",
                "end_time": "2026-03-24 23:59:59",
                "time_slot_list": []
            }
        ]
        
    if prompt_image_base64_list is None:
        prompt_image_base64_list = []

    # 2. 拼接完整的 URL
    url = f"{base_url}/mrag/api/deploy/tasks/create"
    
    # 3. 设置请求头 Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    
    # 4. 组装请求体 Body
    payload = {
        "name": name,
        "deploy_type": deploy_type,
        "left_seconds": left_seconds,
        "right_seconds": right_seconds,
        "target_type": target_type,
        "desc": desc,
        "text": text,
        "image_base64": image_base64,
        "space_time_list": space_time_list,
        "distance": distance,
        "prompt": prompt,
        "prompt_image_base64_list": prompt_image_base64_list,
        "isrealtime": isrealtime
    }

    try:
        # 发送 POST 请求，verify=False 用于跳过 HTTPS(IP) 证书校验
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status() 
        return response.json()      
        
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"服务器返回报错内容: {e.response.text}")
        return None

# ==========================================
# 极简调用示例：
# ==========================================
if __name__ == "__main__":
    
    # 因为所有参数都设置了你的默认值，所以你可以什么参数都不传，直接调用！
    # 它会完全按照你提供的 body 和 header 发送请求。
    print("开始发送默认请求...")
    result = create_deploy_task()
    
    if result:
        print("任务创建成功，返回数据：")
        print(result)
        
    # 当然，如果你想修改某个特定字段，只需像这样传参覆盖即可：
    # result2 = create_deploy_task(name="test_新任务", text="穿红衣服的人", distance=0.5)