import os
import threading
from flask import Flask, jsonify

os.environ['TZ'] = 'Asia/Shanghai'

from DrissionPage import ChromiumPage, ChromiumOptions
import time
import re
from rapidocr import RapidOCR
from PIL import Image

# ================= 1. 定义微服务内存状态 =================
app = Flask(__name__)

# 统一的增量缓冲区：既存查到的违章记录，也存爬虫系统的报错
incremental_buffer = []  
cursor = 0

@app.route('/get_incremental', methods=['GET'])
def get_incremental():
    """CoPaw 心跳会定时请求这个接口拉取数据"""
    global incremental_buffer, cursor
    
    # 提取游标之后的增量数据
    new_data = incremental_buffer[cursor:]
    
    # 更新游标
    cursor = len(incremental_buffer)
    
    return jsonify({
        "count": len(new_data),
        "data": new_data
    })

def start_api_server():
    """在后台静默启动 Flask API 服务"""
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=5050, debug=False, use_reloader=False)

# ================= 2. 爬虫核心逻辑 (基本保留原版逻辑) =================

def ocr_image(image_path, engine):
    img = Image.open(image_path).convert('RGB')
    # 缩放图像到宽=1024
    w, h = img.size
    new_w = 1024
    new_h = int(h * (new_w / w))
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 裁剪图像底部区域
    bottom_height = 128
    bottom_y_start = max(0, new_h - bottom_height)
    bottom_img = resized_img.crop((0, bottom_y_start, new_w, new_h))

    # 裁剪图像中部区域
    mid_y_center = new_h // 2
    mid_y_start = max(0, mid_y_center - 64)
    mid_y_end = min(new_h, mid_y_center + 64)
    middle_img = resized_img.crop((0, mid_y_start, new_w, mid_y_end))
    
    stitch_w = new_w
    stitch_h = bottom_img.height + middle_img.height
    stitch_img = Image.new('RGB', (stitch_w, stitch_h))

    # 图像拼接
    stitch_img.paste(bottom_img, (0, 0))
    stitch_img.paste(middle_img, (0, bottom_img.height))

    # 进行OCR
    result = engine(stitch_img).txts

    if result is None:
        return False

    result = ''.join(result)

    if '违法' in result and '正常' in result:
        return False
    elif '违法' not in result:
        return False
    else:
        return True


def spider_run(start_time_str, end_time_str, place_str, username='370982199305061831', password='Abc@123456', log_callback=None, headless=True):
    def log(msg, level="INFO"):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if log_callback:
            log_callback(msg, level)
        print(f"[{now}] [{level}] {msg}")

    log('接收到的时间字符串为：开始={}, 结束={}'.format(start_time_str, end_time_str))
    engine = RapidOCR()
    
    start_time_str = start_time_str.replace('-', '').replace(':', '').replace(' ', '')
    end_time_str = end_time_str.replace('-', '').replace(':', '').replace(' ', '')

    log('开始登录')
    """指定chrome路径"""
    chrome_path = r'C:\Users\AIIC\AppData\Local\Google\Chrome\Application\chrome.exe'
    co = ChromiumOptions().set_browser_path(chrome_path)

    co.ignore_certificate_errors()
    co.auto_port()

    if headless:
        co.headless()
    
    co.set_argument('--window-size', '1920,1080')
    co.set_argument('--no-sandbox')
    co.set_argument('--ignore-certificate-errors')
    co.set_argument('--ignore-ssl-errors')

    login_page = ChromiumPage(addr_or_opts=co)
    time_zone = login_page.run_js('return Intl.DateTimeFormat().resolvedOptions().timeZone;')
    log('时区为：{}'.format(time_zone))

    login_page.get('https://62.168.12.20:8443/')
    time.sleep(1)
    
    if login_page.title == '62.168.12.20:8443':
        login_page.ele('.form-cut-item-username').ele('.el-input__inner').input(username)
        login_page.ele('.form-cut-item-password').ele('.el-input__inner').input(password)
        wait_time = 15
        for i in range(wait_time):
            time.sleep(1)
        login_page.ele('.form-cut-item-btn').focus().click()
        log('已经点击登录按钮')
        time.sleep(3)

    if '62.168.12.20' != login_page.title:
        log(f'未能成功登录，当前标题: {login_page.title}', "ERROR")
        return
    
    log('成功登录')
    time.sleep(1)
    
    while True:
        try:
            time.sleep(2)
            login_page.ele('text=公共安全视频监控共享平台').click()
            break
        except Exception as e:
            log('未能进入视频综合图像平台', "WARNING")

    time.sleep(4)
    tabs = login_page.get_tabs()
    page = None
    for tab in tabs:
        if tab.title == '视频图像综合应用平台':
            page = tab
            break
    
    if page is None:
        log('未能打开视频图像综合应用平台', "ERROR")
        return

    page.ele('text= 特征搜索 ').click()
    page.ele('.el-input__icon h-icon-arrow_right').click()

    while True:
        try:
            time.sleep(2)
            page.ele('.el-input--width el-input el-input--suffix').click().input(place_str)
            page.ele('.el-input__icon h-icon-search').click()
            break
        except Exception as e:
            pass

    time.sleep(2)
    elements = page.eles('.el-tree-node__content')
    for element in elements:
        if place_str in element.text:
            element.ele('.el-checkbox').click()
            break

    time.sleep(1)
    page.ele("text=确定").parent().click()

    element = page.ele('css:input[placeholder="开始时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(start_time_str)

    element = page.ele('css:input[placeholder="结束时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(end_time_str)

    element = page.ele('.el-button primary_search-but el-button--primary')
    element.click()
    time.sleep(10)

    try:
        page.ele('text= 表格模式 ').click()
    except Exception as e:
        log(f"点击表格模式失败: {e}", "ERROR")
        return
    time.sleep(1)

    page.ele('text= 右侧详情 ').click()
    time.sleep(1)

    old_src = 'placeholder'
    while True:
        persons = page.eles('.el-table__row ') + page.eles('.el-table__row current-row') + page.eles('.el-table__row')
        log('当前页面共发现 {} 条人员记录'.format(len(persons)))
        
        for person_idx, person_row in enumerate(persons):
            while True:
                page.actions.click(person_row.ele('.el-table_1_column_2  '))
                time.sleep(3)
                img_element = page.ele('xpath=//img[@class="iu-img-view__img"]')
                src = img_element.attr('src')
                if src != old_src:
                    old_src = src
                    break
            
            image_path = '{}.png'.format(src.split('/')[-1])
            if os.path.exists(image_path):
                os.remove(image_path)
            page.download(src, verify=False, rename=image_path)
            
            is_caught = ocr_image(image_path, engine)
            if not is_caught:
                continue

            place_name = '未知地点'
            place_element = person_row.ele('css=td.el-table_1_column_3 .cell .plate span')
            if place_element:
                place_name = re.sub(r'\s+', '', place_element.text)
                
            time_str = '19900118092016'
            time_element = person_row.ele('css=td.el-table_1_column_2 .cell .plate span')
            if time_element:
                time_str = re.sub(r'\D+', '', time_element.text)
            
            person_name = "未知身份"
            id_number = "未知身份证号"

            archive_button = person_row.eles('css:button[title="查看档案"]')
            if len(archive_button) > 0:
                archive_button[0].click()
                time.sleep(1)
                person_name_elements = page.eles('.ellipsis')
                time.sleep(4)
                if len(person_name_elements) > 0:
                    person_name = person_name_elements[0].text
                    if person_name != '未知身份':
                        try:
                            id_number = page.ele('text=身份证号').parent().text[4:]
                        except Exception as e:
                            log(f"获取身份证号失败: {e}", "WARNING")

                element = page.ele('css=span.sort-handle[title="特征搜索"]')
                element.click()

                while True:
                    try:
                        element = page.ele('.lidaicon-h-more-vertical btn-icon-more')
                        element.click()
                        time.sleep(2)
                        element = page.ele('关闭其他应用')
                        element.click()
                        break
                    except Exception as e:
                        pass

            image_name = '{}_{}_{}_{}.png'.format(place_name, time_str, id_number, person_name)
            if os.path.exists(image_name):
                os.remove(image_name)
            os.rename(image_path, image_name)
            
            # 【重要修改】：去掉 image_content，只向外层 yield 结构化数据
            yield {
                "event_type": "violation",
                "image_path": image_name,
                "location": place_name,
                "time": time_str,
                "name": person_name,
                "id_number": id_number
            }

        next_page_button = page.ele('.btn-next')
        if next_page_button and next_page_button.attr('disabled') is None:
            next_page_button.click()
            time.sleep(5)
        else:
            log('所有页面处理完毕')
            break

# ================= 3. 主启动函数 =================

def copaw_system_logger(msg, level="INFO"):
    """
    专门给 CoPaw 的回调函数：
    如果爬虫遇到异常 (ERROR/WARNING)，立即写入增量缓冲区，让大模型通知我们。
    """
    if level in ["ERROR", "WARNING"]:
        incremental_buffer.append({
            "event_type": "system_alert",
            "level": level,
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

def run_business_logic():
    global incremental_buffer
    print("开始执行后台爬虫任务...")
    
    # 填入你要持续爬取的时间和地点参数
    for result in spider_run('20260302080000', '20260309235959', '工业路与新华路', headless=False, log_callback=copaw_system_logger):
        
        # 将新发现的违章写入全局列表
        incremental_buffer.append(result)
        print(f"-> 拦截到违章: {result['name']} 位于 {result['location']}")
        
    print("当前批次爬虫任务执行完毕！接口持续保持开启状态供 CoPaw 访问...")

def pedestrian_violation():
    """创建行人违章查询任务"""
    # 1. 在后台线程启动暴露给 AI 的 HTTP 服务
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # 可选：如果你之前开启了浏览器调试，这里可以接管
    # from DrissionPage import Chromium
    # browser = Chromium(9222)
    # tab = browser.latest_tab
    
    # 2. 启动核心爬虫业务逻辑
    run_business_logic()
    
    # 3. 业务跑完后，防止主线程退出导致 API 挂掉
    while True:
        time.sleep(60)