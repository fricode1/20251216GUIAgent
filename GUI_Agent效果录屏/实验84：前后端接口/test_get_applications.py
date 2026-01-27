import requests
import json

# 测试 GET /violation - 查询应用列表
base_url = "http://127.0.0.1:8000/violation"

print("=" * 60)
print("测试 1: 查询应用列表（默认分页）")
print("=" * 60)
try:
    response = requests.get(base_url)
    print(f"状态码: {response.status_code}")
    print(f"响应:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 2: 查询应用列表（指定分页参数）")
print("=" * 60)
params = {
    "pageNo": 1,
    "pageSize": 5
}
print(f"请求参数: {params}")
try:
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    print(f"响应:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 3: 查询第2页（每页3条）")
print("=" * 60)
params = {
    "pageNo": 2,
    "pageSize": 3
}
print(f"请求参数: {params}")
try:
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    if response.status_code == 200 and "data" in data:
        print(f"\n统计信息:")
        print(f"  总记录数: {data['data']['total']}")
        print(f"  当前页码: {data['data']['pageNo']}")
        print(f"  每页条数: {data['data']['pageSize']}")
        print(f"  当前页记录数: {len(data['data']['list'])}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 4: 验证应用状态字段")
print("=" * 60)
try:
    response = requests.get(base_url, params={"pageSize": 10})
    if response.status_code == 200:
        data = response.json()
        if data['data']['list']:
            print("应用列表中的状态值:")
            for app in data['data']['list']:
                print(f"  ID: {app['id']}, 名称: {app['name']}, 状态: {app['status']}")
        else:
            print("当前没有任何应用记录")
except Exception as e:
    print(f"错误: {e}")
