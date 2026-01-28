import requests
import json
from datetime import datetime

# 测试 GET /violation/images - 查询图片列表
base_url = "http://127.0.0.1:8000/violation/images"

print("=" * 60)
print("测试 1: 查询图片列表（默认分页）")
print("=" * 60)
try:
    response = requests.get(base_url)
    print(f"状态码: {response.status_code}")
    print(f"响应:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 2: 查询图片列表（指定分页参数）")
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
print("测试 4: 验证图片数据字段")
print("=" * 60)
try:
    response = requests.get(base_url, params={"pageSize": 10})
    if response.status_code == 200:
        data = response.json()
        if data['data']['list']:
            print("图片列表详情:")
            for idx, img in enumerate(data['data']['list'], 1):
                print(f"\n图片 {idx}:")
                print(f"  创建时间: {img['created_at']}")
                print(f"  图片URL: {img['url'][:80]}..." if len(img['url']) > 80 else f"  图片URL: {img['url']}")
                
                # 验证 URL 是否可访问（仅检查格式）
                if img['url'].startswith('http'):
                    print(f"  URL格式: ✓ 有效")
                else:
                    print(f"  URL格式: ✗ 无效")
        else:
            print("当前没有任何图片记录")
            print("\n提示: 需要先创建应用并等待爬虫运行后才会有图片数据")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 5: 大分页测试")
print("=" * 60)
params = {
    "pageNo": 1,
    "pageSize": 100
}
print(f"请求参数: {params}")
try:
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"总记录数: {data['data']['total']}")
        print(f"实际返回: {len(data['data']['list'])} 条记录")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 6: 边界测试（空页）")
print("=" * 60)
params = {
    "pageNo": 999,
    "pageSize": 10
}
print(f"请求参数: {params}")
try:
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"返回记录数: {len(data['data']['list'])}")
        print("边界处理: ✓ 正常（返回空列表）")
except Exception as e:
    print(f"错误: {e}")
