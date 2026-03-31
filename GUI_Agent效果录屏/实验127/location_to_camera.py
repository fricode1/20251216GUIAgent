import requests
import urllib3

# 禁用因 verify=False 产生的不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImU3OGZlOWYxLWE1YzAtNDg0OS1iMTUxLTE3MmZkZjY3MTIzNiJ9.FgNeLLZAiaI3VE3fBZONZ7aWHiROGjIFso0hnv1D1yZXmLvQhe9Z0SSMXINucSrvIkCP_ab5LCsmeFk-tPhoyQ",
        "Content-Type": "application/json"
    }
    
    # 设置请求载荷 (payload)
    payload = {
        "pageNumber": 1,
        "pageSize": 1,
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
                return data_list[0].get("apeId")
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