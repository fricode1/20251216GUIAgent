import time
from DrissionPage import Chromium

person_name = '张三丰'

print("正在初始化浏览器...")
browser = Chromium()
tab = browser.latest_tab
print("浏览器初始化完成。")

print("正在进入登录页...")
login_result = tab.get('https://62.168.12.20:8443/', retry=1, timeout=4)
if not login_result:
    print("登录页连接失败，程序退出。")
    browser.quit()
    exit()
print("已进入登录页。")

current_url = tab.url
print(f"当前页面URL: {current_url}")

if 'home' in current_url:
    print("检测到已登录，直接跳转到应用市场页。")
else:
    print("需要执行登录操作。")
    
    print("正在输入用户名...")
    username_input = tab.ele('.form-cut-item-username').ele('.el-input__inner')
    username_input.input('370982199305061831')
    print("用户名输入完成。")
    
    print("正在输入密码...")
    password_input = tab.ele('.form-cut-item-password').ele('.el-input__inner')
    password_input.input('Abc@123456')
    print("密码输入完成。")
    
    print("等待15秒...")
    time.sleep(15)
    
    print("正在点击登录按钮...")
    login_btn = tab.ele('.form-cut-item-btn')
    login_btn.focus().click()
    print("登录按钮点击完成。")
    
    time.sleep(5)
    print("登录完成，等待页面跳转。")

print("正在进入应用市场页...")
time.sleep(3)
print("应用市场页加载完成。")

print("正在点击'公共安全视频监控共享平台'按钮...")
platform_btn = tab.ele('text=公共安全视频监控共享平台')
platform_btn.click()
print("按钮点击完成，等待新标签页打开。")

print("等待新标签页打开...")
time.sleep(5)
tab = browser.latest_tab
time.sleep(3)
print("已切换到视综平台标签页。")

print("正在点击身份确认按钮...")
confirm_btns = tab.eles('身份确认')
if len(confirm_btns) > 1:
    confirm_btns[1].click()
    print("身份确认按钮点击完成。")
else:
    print("未找到身份确认按钮，程序退出。")
    browser.quit()
    exit()

time.sleep(3)
print("已进入身份确认页面。")

print(f"正在输入姓名: {person_name}...")
name_input = tab.ele('@placeholder=请输入精确姓名')
name_input.click().input(person_name)
print("姓名输入完成。")

print("正在点击查询按钮...")
query_btn = tab.ele(' 查询 ')
query_btn.click()
print("查询按钮点击完成，等待查询结果。")

time.sleep(5)
print("正在获取所有人员卡片...")
person_cards = tab.eles('@class:basic-wrap id-l-content__card hover')
print(f"共找到 {len(person_cards)} 张人员卡片。")

print("\n开始提取人员信息...")
for i, card in enumerate(person_cards, 1):
    print(f"\n--- 人员 {i} ---")
    
    try:
        img_ele = card.ele('tag:img')
        print("已获取图像元素。")
    except Exception as e:
        print(f"获取图像失败: {e}")
    
    try:
        name_ele = card.ele('@class:text-ellipsis')
        name_text = name_ele.text
        print(f"姓名: {name_text}")
    except Exception as e:
        print(f"获取姓名失败: {e}")
        name_text = "未知"
    
    try:
        id_ele = card.ele('@class:text_certificateNumber')
        id_text = id_ele.text
        print(f"身份证号: {id_text}")
    except Exception as e:
        print(f"获取身份证号失败: {e}")
        id_text = "未知"

print("\n" + "="*50)
print("执行总结:")
print(f"1. 浏览器初始化成功")
print(f"2. 登录流程执行完成")
print(f"3. 成功切换到视综平台")
print(f"4. 查询姓名: {person_name}")
print(f"5. 共找到 {len(person_cards)} 条记录")
print(f"6. 所有人员信息提取完成")
print("="*50)

print("\n脚本执行完毕。")