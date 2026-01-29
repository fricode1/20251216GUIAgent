
from DrissionPage import ChromiumPage, ChromiumOptions
import time

# 设置浏览器选项
co = ChromiumOptions()
co.headless(False)  # 非无头模式

# 创建页面对象
browser = ChromiumPage(addr_or_opts=co)

# 定义查询姓名
person_name = '张三丰'

try:
    # 1. 进入登录页
    tab = browser.get('https://62.168.12.20:8443/')
    
    # 2. 输入用户名
    username_input = tab.ele('.form-cut-item-username').ele('.el-input__inner')
    username_input.input('370982199305061831')
    
    # 3. 输入密码
    password_input = tab.ele('.form-cut-item-password').ele('.el-input__inner')
    password_input.input('Abc@123456')
    
    # 4. 等待15秒后点击登录
    time.sleep(15)
    login_btn = tab.ele('.form-cut-item-btn')
    login_btn.focus().click()
    
    # 5. 点击公共安全视频监控平台
    time.sleep(5)  # 等待页面加载
    app_btn = tab.ele('text=公共安全视频监控共享平台')
    app_btn.click()
    
    # 6. 切换到新标签页
    time.sleep(3)
    tab = browser.latest_tab
    
    # 7. 点击身份确认按钮
    time.sleep(5)  # 等待页面加载
    confirm_btns = tab.eles('身份确认')
    if len(confirm_btns) > 1:
        confirm_btns[1].click()
    
    # 8. 输入姓名并查询
    time.sleep(3)
    name_input = tab.ele('@placeholder=请输入精确姓名')
    name_input.click().input(person_name)
    
    query_btn = tab.ele(' 查询 ')
    query_btn.click()
    
    # 9. 获取所有人员卡片
    time.sleep(5)
    person_cards = tab.eles('@class:basic-wrap id-l-content__card hover')
    
    # 10. 遍历每个卡片提取信息
    results = []
    for person_card in person_cards:
        try:
            # 获取图像
            img_element = person_card.ele('tag:img')
            img_src = img_element.attr('src') if img_element else None
            
            # 获取行人信息
            name_element = person_card.ele('@class:text-ellipsis')
            name = name_element.text if name_element else None
            
            # 获取身份证号
            id_element = person_card.ele('@class:text_certificateNumber')
            id_number = id_element.text if id_element else None
            
            if name and id_number:
                results.append({
                    'name': name,
                    'id_number': id_number,
                    'img_src': img_src
                })
                print(f"姓名: {name}, 身份证号: {id_number}")
                
        except Exception as e:
            print(f"处理卡片时出错: {e}")
            continue
    
    print(f"共找到 {len(results)} 条记录")
    
except Exception as e:
    print(f"脚本执行出错: {e}")

finally:
    # 保持浏览器打开以便查看结果
    input("按Enter键关闭浏览器...")
    browser.quit()
