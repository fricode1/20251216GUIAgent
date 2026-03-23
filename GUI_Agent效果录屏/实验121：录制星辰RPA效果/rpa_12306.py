# 文件路径示例: /opt/scripts/query_ticket.py
import requests
import sys
import json

def main():
    # 检查参数数量 (脚本名 + 3个参数)
    if len(sys.argv) != 4:
        print("用法: python query_ticket.py <出发地> <到达地> <出发日期(YYYY-MM-DD)>")
        sys.exit(1)

    from_station = sys.argv[1]
    to_station = sys.argv[2]
    start_date = sys.argv[3]

    url = "http://172.20.118.153:32742/api/rpa-openapi/workflows/execute"
    headers = {
        "Authorization": "Bearer 931bba7rX73k15oAsJR8KkfXiSZBwhG0",
        "Content-Type": "application/json"
    }
    
    data = {
        "project_id": "2034832313526808576",
        "params": {
            "input_variable": from_station,
            "to_station": to_station,
            "start_date": start_date
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        # 使用 ensure_ascii=False 确保输出中文不乱码，方便 AI 解析
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    main()