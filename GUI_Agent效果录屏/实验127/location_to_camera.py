import requests
import urllib3
import config

# 禁用因 verify=False 产生的不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def response_simplify(camera_list):
    """
    input: 
        camera_list: list of dict
    """
    simple_result = []
    for camera_item in camera_list:
        camera_name = camera_item.get("name")
        camera_id = camera_item.get("apeId")
        simple_result.append({"apeId": camera_id, "name": camera_name})
    return simple_result


def location_to_camera(location):
    """根据地点查询摄像头ID
    input:
        location: str
    return:
        camera_id: str
    """
    url = "https://62.168.243.10:19080/data/api/v1/device/list"
    
    # 设置请求头
    headers = {
        "Authorization": config.authorization,
        "Content-Type": "application/json"
    }
    
    # 设置请求载荷 (payload)
    payload = {
        "pageNumber": 1,
        "pageSize": 3,
        "queryCondition": location
    }
    
    try:
        # 发起 POST 请求
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            verify=False, # 忽略自签名证书导致的 SSL 验证错误
            timeout=10    # 设置超时时间
        )
        
        # 确保 HTTP 请求成功
        response.raise_for_status()
        
        # 解析 JSON 响应
        res_json = response.json()
        
        # 验证接口业务状态码并提取 apeId
        if res_json.get("code") == "0":
            data_list = res_json.get("data", {}).get("list", [])
            if data_list:
                simple_result = response_simplify(data_list)
                return simple_result
                # return data_list[0].get("apeId")
            else:
                # 列表为空，说明没查到该地点
                return None
        else:
            print(f"接口返回错误: {res_json.get('msg')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

# ====================
# 测试用例
# ====================
if __name__ == "__main__":
    result = location_to_camera("新华路")
    print(f"输出：{result}")