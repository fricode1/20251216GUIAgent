
from DrissionPage import Chromium
import time

person_name = '张三丰'

print("正在初始化浏览器...")
browser = Chromium()
tab = browser.latest_tab
print("浏览器初始化完成。")

print("正在进入登录页...")
login_result = tab.get('https://62.168.12.20:8443/', retry=0, timeout=2)
if not login_result:
    print("登录页连接失败，退出脚本。")
    browser.quit()
    exit()
print("已进入登录页。")

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
print("等待结束。")

print("正在点击登录按钮...")
login_button = tab.ele('.form-cut-item-btn')
login_button.focus().click()
print("登录按钮点击完成。")

print("等待登录后页面加载...")
time.sleep(5)
print("登录完成，已进入应用市场页。")

print("正在点击'公共安全视频监控共享平台'按钮...")
app_button = tab.ele('text=公共安全视频监控共享平台')
app_button.click()
print("按钮点击完成，等待新标签页打开...")
time.sleep(3)

print("切换到视综平台标签页...")
tab = browser.latest_tab
print("已切换到视综平台标签页。")

print("正在点击身份确认按钮...")
confirm_buttons = tab.eles('身份确认')
if len(confirm_buttons) > 1:
    confirm_buttons[1].click()
    print("身份确认按钮点击完成。")
else:
    print("未找到身份确认按钮，退出脚本。")
    browser.quit()
    exit()

print("等待身份确认页面加载...")
time.sleep(3)
print("已进入身份确认页面。")

print(f"正在输入姓名: {person_name}...")
name_input = tab.ele('@placeholder=请输入精确姓名')
name_input.click().input(person_name)
print("姓名输入完成。")

print("正在点击查询按钮...")
query_button = tab.ele(' 查询 ')
query_button.click()
print("查询按钮点击完成，等待查询结果...")
time.sleep(5)

print("正在获取所有人员卡片...")
person_cards = tab.eles('@class:basic-wrap id-l-content__card hover')
print(f"共找到 {len(person_cards)} 张人员卡片。")

person_info_list = []

for idx, person_card in enumerate(person_cards, start=1):
    print(f"正在处理第 {idx} 张卡片...")
    
    try:
        img_element = person_card.ele('tag:img')
        img_src = img_element.attr('src') if img_element else "未找到图像"
        print(f"  卡片 {idx} 图像: {img_src[:50]}...")
    except Exception as e:
        img_src = f"获取图像失败: {e}"
        print(f"  卡片 {idx} 图像获取失败。")
    
    try:
        name_element = person_card.ele('@class:text-ellipsis')
        name = name_element.text if name_element else "未找到姓名"
        print(f"  卡片 {idx} 姓名: {name}")
    except Exception as e:
        name = f"获取姓名失败: {e}"
        print(f"  卡片 {idx} 姓名获取失败。")
    
    try:
        id_element = person_card.ele('@class:text_certificateNumber')
        id_number = id_element.text if id_element else "未找到身份证号"
        print(f"  卡片 {idx} 身份证号: {id_number}")
    except Exception as e:
        id_number = f"获取身份证号失败: {e}"
        print(f"  卡片 {idx} 身份证号获取失败。")
    
    person_info = {
        'index': idx,
        'name': name,
        'id_number': id_number,
        'img_src': img_src
    }
    person_info_list.append(person_info)
    print(f"  卡片 {idx} 处理完成。")

print("\n" + "="*50)
print("执行总结:")
print(f"  查询姓名: {person_name}")
print(f"  找到卡片数量: {len(person_cards)}")
print(f"  成功处理卡片数量: {len(person_info_list)}")
print("="*50)

for info in person_info_list:
    print(f"卡片 {info['index']}: 姓名={info['name']}, 身份证号={info['id_number']}")

print("\n脚本执行完毕。")
