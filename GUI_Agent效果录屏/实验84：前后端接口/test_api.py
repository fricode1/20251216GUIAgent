import requests
import json

# 测试 POST /violation
url = "http://127.0.0.1:8000/violation"

# 正确的请求格式（根据接口文档）
data = {
    "name": "测试应用",
    "start_time": "2026-01-27 10:00:00",
    "end_time": "2026-01-27 18:00:00",
    "address": "凤瑞路七峰大道东南角向北"
}

print("发送请求:")
print(json.dumps(data, indent=2, ensure_ascii=False))

try:
    response = requests.post(url, json=data)
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 422:
        print("\n422 详细错误:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误: {e}")
