import time
from DrissionPage import Chromium

def main():
    print("开始执行身份确认脚本...")
    
    # 1. 打开浏览器
    print("正在打开浏览器...")
    browser = Chromium()
    tab = browser.latest_tab
    print("浏览器已打开")
    
    # 2. 进入登录页
    print("正在进入登录页...")
    result = tab.get('https://62.168.12.20:8443/', retry=1, timeout=4)
    
    if result is False:
        print("无法连接到登录页，脚本终止")
        return
    
    print("成功连接到登录页")
    
    # 3. 检查是否需要登录
    current_url = tab.url
    print(f"当前URL: {current_url}")
    
    if 'home' in current_url:
        print("检测到已登录，跳过登录步骤")
    else:
        print("需要执行登录操作...")
        
        # 输入用户名
        print("正在输入用户名...")
        try:
            username_input = tab.ele('.form-cut-item-username').ele('.el-input__inner')
            username_input.input('370982199305061831')
            print("用户名输入完成")
        except Exception as e:
            print(f"输入用户名失败: {e}")
            return
            
        # 输入密码
        print("正在输入密码...")
        try:
            password_input = tab.ele('.form-cut-item-password').ele('.el-input__inner')
            password_input.input('Abc@123456')
            print("密码输入完成")
        except Exception as e:
            print(f"输入密码失败: {e}")
            return
            
        # 等待15秒
        print("等待15秒...")
        time.sleep(15)
        
        # 点击登录按钮
        print("正在点击登录按钮...")
        try:
            login_btn = tab.ele('.form-cut-item-btn')
            login_btn.focus().click()
            print("登录按钮点击完成")
        except Exception as e:
            print(f"点击登录按钮失败: {e}")
            return
            
        time.sleep(5)
        print("登录完成")
    
    # 4. 进入应用市场页
    print("等待应用市场页加载...")
    time.sleep(3)
    
    # 5. 点击公共安全视频监控平台按钮
    print("正在点击公共安全视频监控共享平台按钮...")
    try:
        platform_btn = tab.ele('text=公共安全视频监控共享平台')
        platform_btn.click()
        print("平台按钮点击完成")
    except Exception as e:
        print(f"点击平台按钮失败: {e}")
        return
    
    # 6. 切换到视综平台标签页
    print("切换到视综平台标签页...")
    time.sleep(5)
    tab = browser.latest_tab
    time.sleep(3)
    print(f"已切换到新标签页，当前URL: {tab.url}")
    
    # 7. 点击身份确认按钮
    print("正在点击身份确认按钮...")
    try:
        identity_btns = tab.eles('身份确认')
        if len(identity_btns) >= 2:
            identity_btns[1].click()
            print("身份确认按钮点击完成")
        else:
            print(f"未找到足够的身份确认按钮，只找到 {len(identity_btns)} 个")
            return
    except Exception as e:
        print(f"点击身份确认按钮失败: {e}")
        return
    
    time.sleep(5)
    print("进入身份确认页面")
    
    # 8. 根据姓名查询（用户提供的是姓名）
    target_name = "张三丰"
    print(f"开始根据姓名查询: {target_name}")
    
    # 输入姓名
    print("正在输入查询姓名...")
    try:
        name_input = tab.ele('@placeholder=请输入精确姓名')
        name_input.click().input(target_name)
        print("姓名输入完成")
    except Exception as e:
        print(f"输入姓名失败: {e}")
        return
    
    # 点击查询按钮
    print("正在点击查询按钮...")
    try:
        search_btn = tab.ele(' 查询 ')
        search_btn.click()
        print("查询按钮点击完成")
    except Exception as e:
        print(f"点击查询按钮失败: {e}")
        return
    
    time.sleep(3)
    
    # 9. 获取所有卡片
    print("正在获取查询结果卡片...")
    try:
        person_cards = tab.eles('@class:basic-wrap id-l-content__card hover')
        card_count = len(person_cards)
        print(f"找到 {card_count} 个匹配的卡片")
    except Exception as e:
        print(f"获取卡片失败: {e}")
        return
    
    results = []
    
    # 10. 提取每个卡片的信息
    for i, card in enumerate(person_cards):
        print(f"处理第 {i+1} 个卡片...")
        
        try:
            # 获取图像
            img_element = card.ele('tag:img')
            img_src = img_element.attr('src') if img_element else "未找到图像"
            print(f"  图像来源: {img_src[:50] if img_src else '无'}")
            
            # 获取姓名
            name_element = card.ele('@class:text-ellipsis')
            name = name_element.text if name_element else "未找到姓名"
            print(f"  姓名: {name}")
            
            # 获取身份证号
            id_element = card.ele('@class:text_certificateNumber')
            id_number = id_element.text if id_element else "未找到身份证号"
            print(f"  身份证号: {id_number}")
            
            results.append({
                '序号': i+1,
                '姓名': name,
                '身份证号': id_number,
                '图像': img_src
            })
            
        except Exception as e:
            print(f"  处理卡片 {i+1} 时出错: {e}")
            results.append({
                '序号': i+1,
                '姓名': '处理出错',
                '身份证号': '处理出错',
                '图像': '处理出错'
            })
    
    # 11. 打印执行总结
    print("\n" + "="*50)
    print("执行总结:")
    print(f"目标查询姓名: {target_name}")
    print(f"找到的匹配人数: {len(results)}")
    print("\n查询结果详情:")
    
    for result in results:
        print(f"\n人员 {result['序号']}:")
        print(f"  姓名: {result['姓名']}")
        print(f"  身份证号: {result['身份证号']}")
        print(f"  图像: {result['图像'][:80] if result['图像'] != '处理出错' else '处理出错'}")
    
    print("\n脚本执行完成")
    print("="*50)

if __name__ == "__main__":
    main()