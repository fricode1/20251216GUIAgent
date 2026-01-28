import requests
import json
import time

# 测试 DELETE /violation/{id} - 删除应用
base_url = "http://127.0.0.1:8000/violation"

print("=" * 60)
print("准备工作: 先创建几个测试应用")
print("=" * 60)

# 创建3个测试应用
created_ids = []
for i in range(1, 4):
    data = {
        "name": f"测试应用_{i}",
        "start_time": "2026-01-27 10:00:00",
        "end_time": "2026-01-27 18:00:00",
        "address": f"测试地址_{i}"
    }
    try:
        response = requests.post(base_url, json=data)
        if response.status_code == 200:
            print(f"✓ 创建应用 {i} 成功")
            # 获取创建的应用ID（需要查询列表）
            time.sleep(0.5)
        else:
            print(f"✗ 创建应用 {i} 失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 创建应用 {i} 出错: {e}")

# 查询当前所有应用，获取ID
time.sleep(1)
try:
    response = requests.get(base_url, params={"pageSize": 100})
    if response.status_code == 200:
        data = response.json()
        created_ids = [app['id'] for app in data['data']['list']]
        print(f"\n当前系统中共有 {len(created_ids)} 个应用")
        print(f"应用ID列表: {created_ids}")
except Exception as e:
    print(f"查询应用列表失败: {e}")

if not created_ids:
    print("\n警告: 没有可用的应用进行删除测试")
    exit(0)

print("\n" + "=" * 60)
print("测试 1: 删除存在的应用")
print("=" * 60)
if len(created_ids) >= 1:
    test_id = created_ids[0]
    print(f"删除应用 ID: {test_id}")
    try:
        response = requests.delete(f"{base_url}/{test_id}")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✓ 删除成功")
            
            # 验证是否真的删除了
            time.sleep(0.5)
            verify_response = requests.get(base_url)
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                remaining_ids = [app['id'] for app in verify_data['data']['list']]
                if test_id not in remaining_ids:
                    print(f"✓ 验证成功: 应用 {test_id} 已从列表中移除")
                else:
                    print(f"✗ 验证失败: 应用 {test_id} 仍在列表中")
    except Exception as e:
        print(f"错误: {e}")
else:
    print("跳过: 没有足够的应用")

print("\n" + "=" * 60)
print("测试 2: 删除不存在的应用（边界测试）")
print("=" * 60)
non_existent_id = 99999
print(f"尝试删除不存在的应用 ID: {non_existent_id}")
try:
    response = requests.delete(f"{base_url}/{non_existent_id}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 404:
        print("✓ 正确处理: 返回 404 Not Found")
    elif response.status_code == 200:
        print("⚠ 警告: 应返回 404，但返回了 200")
    else:
        print(f"⚠ 意外状态码: {response.status_code}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试 3: 验证级联删除（删除应用时关联图片也被删除）")
print("=" * 60)
if len(created_ids) >= 2:
    test_id = created_ids[1]
    print(f"删除应用 ID: {test_id}")
    
    # 先查询该应用关联的图片数量
    try:
        images_response = requests.get(f"{base_url}/images", params={"pageSize": 1000})
        if images_response.status_code == 200:
            images_before = images_response.json()['data']['total']
            print(f"删除前系统图片总数: {images_before}")
    except Exception as e:
        print(f"查询图片失败: {e}")
        images_before = 0
    
    # 删除应用
    try:
        response = requests.delete(f"{base_url}/{test_id}")
        if response.status_code == 200:
            print(f"✓ 应用 {test_id} 删除成功")
            
            # 等待级联删除完成
            time.sleep(1)
            
            # 再次查询图片数量
            images_response = requests.get(f"{base_url}/images", params={"pageSize": 1000})
            if images_response.status_code == 200:
                images_after = images_response.json()['data']['total']
                print(f"删除后系统图片总数: {images_after}")
                
                if images_after <= images_before:
                    print("✓ 级联删除验证: 关联图片已被删除或无变化")
                else:
                    print("⚠ 警告: 图片数量反而增加了")
    except Exception as e:
        print(f"错误: {e}")
else:
    print("跳过: 没有足够的应用")

print("\n" + "=" * 60)
print("测试 4: 批量删除测试")
print("=" * 60)
# 获取当前所有应用
try:
    response = requests.get(base_url, params={"pageSize": 100})
    if response.status_code == 200:
        data = response.json()
        current_ids = [app['id'] for app in data['data']['list']]
        print(f"当前剩余 {len(current_ids)} 个应用")
        
        if current_ids:
            print("开始批量删除...")
            success_count = 0
            fail_count = 0
            
            for app_id in current_ids:
                try:
                    del_response = requests.delete(f"{base_url}/{app_id}")
                    if del_response.status_code == 200:
                        success_count += 1
                        print(f"  ✓ 删除应用 {app_id} 成功")
                    else:
                        fail_count += 1
                        print(f"  ✗ 删除应用 {app_id} 失败: {del_response.status_code}")
                    time.sleep(0.2)
                except Exception as e:
                    fail_count += 1
                    print(f"  ✗ 删除应用 {app_id} 出错: {e}")
            
            print(f"\n批量删除结果: 成功 {success_count}, 失败 {fail_count}")
            
            # 验证是否全部删除
            time.sleep(1)
            verify_response = requests.get(base_url)
            if verify_response.status_code == 200:
                remaining = verify_response.json()['data']['total']
                print(f"剩余应用数: {remaining}")
                if remaining == 0:
                    print("✓ 所有应用已清空")
                else:
                    print(f"⚠ 仍有 {remaining} 个应用未删除")
        else:
            print("当前没有应用需要删除")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
