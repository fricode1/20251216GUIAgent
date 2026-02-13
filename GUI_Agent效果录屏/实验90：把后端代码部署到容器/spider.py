import os
os.environ['TZ'] = 'Asia/Shanghai'

from DrissionPage import ChromiumPage, ChromiumOptions
import time
import re
from rapidocr import RapidOCR
from PIL import Image


def ocr_image(image_path, engine):
    img = Image.open(image_path).convert('RGB')


    # 缩放图像到宽=1024
    w, h = img.size
    new_w = 1024
    new_h = int(h * (new_w / w))
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 裁剪图像底部区域，从x1y1=(0, h-128)到x2y2=(w, h)
    bottom_height = 128
    bottom_y_start = max(0, new_h - bottom_height)  # 防止负值
    bottom_img = resized_img.crop(
        (0, bottom_y_start, new_w, new_h)
    )

    # 裁剪图像中部区域，从x1y1=(0，h//2-64)到x2y2=(w,h//2+64)
    mid_y_center = new_h // 2
    mid_y_start = max(0, mid_y_center - 64)  # 防止负值
    mid_y_end = min(new_h, mid_y_center + 64)  # 防止超出图像范围
    middle_img = resized_img.crop(
        (0, mid_y_start, new_w, mid_y_end)
    )
    stitch_w = new_w
    stitch_h = bottom_img.height + middle_img.height
    stitch_img = Image.new('RGB', (stitch_w, stitch_h))

    # 图像拼接
    stitch_img.paste(bottom_img, (0, 0))
    stitch_img.paste(middle_img, (0, bottom_img.height))

    # 进行OCR
    result = engine(stitch_img).txts

    if result is None:
        return False  # 没有违法

    result = ''.join(result)

    # debug
    # print(stitch_img.width, stitch_img.height)
    # print(result)

    if '违法' in result and '正常' in result:
        return False  # 没有违法
    elif '违法' not in result:
        return False  # 没有违法
    else:
        return True


def spider_run_dummy(start_time_str, end_time_str, place_str, username='370982199305061831', password='Abc@123456', log_callback=None):
    def log(msg, level="INFO"):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if log_callback:
            log_callback(msg, level)
        print(f"[{now}] [{level}] {msg}")

    # ==================== 3. 遍历所有页面抓取数据 ====================
    while True:
        for person_idx in range(10):

            with open('/home/zcc/zhbli/projects/实验84：前后端接口/backend/4.png', 'rb') as f:
                image_content = f.read()

            log('开始返回')
            
            yield {
                "status": "success",
                "image_name": "1",
                "image_content": image_content,
                "location": "place_name",
                "time": "time_str",
                "name": "person_name",
                "id_number": "id_number"
            }


        time.sleep(3)


def spider_run(start_time_str, end_time_str, place_str, username='370982199305061831', password='Abc@123456', log_callback=None, headless=True):
    """
    完整的爬虫流程：登录 -> 搜索 -> 抓取 -> 返回结果
    
    Args:
        start_time_str: 开始时间字符串，格式 '20250123010203' (YYYYMMDDHHmmss)
        end_time_str: 结束时间字符串，格式 '20250123235959' (YYYYMMDDHHmmss)
        place_str: 地点字符串，如 '凤瑞路七峰大道东南角向北'
        username: 登录用户名
        password: 登录密码
        log_callback: 日志回调函数 (message, level)
    
    Yields:
        dict: 包含图片信息的字典
    """
    def log(msg, level="INFO"):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if log_callback:
            log_callback(msg, level)
        print(f"[{now}] [{level}] {msg}")

    log('接收到的时间字符串为：开始={}, 结束={}'.format(start_time_str, end_time_str))

    engine = RapidOCR()
    
    # ==================== 1. 登录流程 ====================
    
    # 转换时间格式：'2026-01-02 01:02:03' -> '20260102010203'
    start_time_str = start_time_str.replace('-', '').replace(':', '').replace(' ', '')
    end_time_str = end_time_str.replace('-', '').replace(':', '').replace(' ', '')

    log('开始登录')
    co = ChromiumOptions()
    co.ignore_certificate_errors()
    co.auto_port()

    # 有时调试时不希望是headless模式
    if headless:
        co.headless()
    
    co.set_argument('--window-size', '1920,1080')
    co.set_argument('--no-sandbox')
    co.set_argument('--ignore-certificate-errors')
    co.set_argument('--ignore-ssl-errors')

    login_page = ChromiumPage(addr_or_opts=co)

    time_zone = login_page.run_js('return Intl.DateTimeFormat().resolvedOptions().timeZone;')
    log('时区为：{}'.format(time_zone))
    print('时区为：{}'.format(time_zone))

    log('开始进入登录页面')
    login_page.get('https://62.168.12.20:8443/')
    time.sleep(1)
    log(f"页面标题: {login_page.title}")
    
    if login_page.title == '62.168.12.20:8443':
        login_page.ele('.form-cut-item-username').ele('.el-input__inner').input(username)
        login_page.ele('.form-cut-item-password').ele('.el-input__inner').input(password)
        wait_time = 15
        log('已经输入用户名和密码，正在等待{}秒'.format(wait_time))
        for i in range(wait_time):
            log(f"等待中... {i+1}")
            time.sleep(1)
        login_page.ele('.form-cut-item-btn').focus().click()
        log('已经点击登录按钮')
        time.sleep(3)

    if '62.168.12.20' != login_page.title:
        log(f'未能成功登录，当前标题: {login_page.title}', "ERROR")
        return
    
    log('成功登录')
    log('进入视综平台')
    time.sleep(1)
    
    while True:
        try:
            time.sleep(2)
            login_page.ele('text=公共安全视频监控共享平台').click()
            log('已经进入视频综合图像平台')
            break
        except Exception as e:
            log('未能进入，报错信息为：{}。当前页面内容为：{}'.format(e, login_page.text), "WARNING")

    time.sleep(4)

    tabs = login_page.get_tabs()
    log('已经打开的标签页如下：')
    page = None
    for tab in tabs:
        log(f"标签页: {tab.title}")
        if tab.title == '视频图像综合应用平台':
            page = tab
            break
    
    if page is None:
        log('未能打开视频图像综合应用平台', "ERROR")
        return

    # ==================== 2. 进入特征搜索并设置参数 ====================
    log(f"当前页面: {page.title}")
    page.ele('text= 特征搜索 ').click()
    log('进入特征搜索')

    # 设置地点
    log('开始设置地点')
    page.ele('.el-input__icon h-icon-arrow_right').click()

    while True:
        try:
            time.sleep(2)
            page.ele('.el-input--width el-input el-input--suffix').click().input(place_str)
            page.ele('.el-input__icon h-icon-search').click()
            break
        except Exception as e:
            log(f'等待"选择点位"动态元素加载: {e}', "DEBUG")

    # 选中摄像机
    time.sleep(2)
    elements = page.eles('.el-tree-node__content')
    for element in elements:
        if place_str in element.text:
            element.ele('.el-checkbox').click()
            break

    # 点击确定按钮
    time.sleep(1)
    page.ele("text=确定").parent().click()
    log('完成设置地点')

    # 设置开始时间
    element = page.ele('css:input[placeholder="开始时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(start_time_str)
    log('开始时间设置为：{}'.format(start_time_str))

    # 设置结束时间
    element = page.ele('css:input[placeholder="结束时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(end_time_str)
    log('结束时间设置为：{}'.format(end_time_str))

    # 点击查询按钮
    element = page.ele('.el-button primary_search-but el-button--primary')
    element.click()
    log('已点击查询按钮，等待数据加载...')
    time.sleep(10)

    # 点击 表格模式 按钮
    log('开始点击"表格模式"按钮')
    try:
        page.ele('text= 表格模式 ').click()
    except Exception as e:
        page.get_screenshot()
        log(f"点击表格模式失败: {e}", "ERROR")
        return
    time.sleep(1)

    # 点击 右侧详情 按钮
    page.ele('text= 右侧详情 ').click()
    time.sleep(1)

    # ==================== 3. 遍历所有页面抓取数据 ====================
    old_src = 'palceholder'  # 常出现的问题是，如果前面对行的点击没有生效，则抓拍照是旧的。因此需要进行循环判断抓拍照是否被更新。为此就要初始化一个src
    while True:
        # 处理当前页面
        persons = page.eles('.el-table__row ') + page.eles('.el-table__row current-row') + page.eles('.el-table__row')
        log('当前页面共发现 {} 条人员记录'.format(len(persons)))
        
        for person_idx, person_row in enumerate(persons):
            log('----------- 处理行人 {} ------------'.format(person_idx + 1))
            while True:
                page.actions.click(person_row.ele('.el-table_1_column_2  '))  # 这句话很关键。直接点击person_row不行，点击person_row的第一个元素也不行。这是魏鹏帮忙试出来的。
                time.sleep(3)
                img_element = page.ele('xpath=//img[@class="iu-img-view__img"]')
                src = img_element.attr('src')
                if src != old_src:
                    old_src = src
                    break
            log(f"图片源地址: {src}", "DEBUG")
            image_path = '{}.png'.format(src.split('/')[-1])
            if os.path.exists(image_path):
                os.remove(image_path)
            page.download(src, verify=False, rename=image_path)
            is_caught = ocr_image(image_path, engine)
            if not is_caught:
                log('OCR检测结果：未发现违法抓拍标记，跳过')
                continue
            else:
                log('OCR检测结果：确认存在违法抓拍标记！')

            # 获取抓拍地点和时间
            place_name = '未知地点'
            place_element = person_row.ele('css=td.el-table_1_column_3 .cell .plate span')
            if place_element:
                place_name = place_element.text
                place_name = re.sub(r'\s+', '', place_name)
            time_str = '19900118092016'
            time_element = person_row.ele('css=td.el-table_1_column_2 .cell .plate span')
            if time_element:
                time_str = time_element.text
                time_str = re.sub(r'\D+', '', time_str)
            
            """START: 获取姓名与身份证号"""
            person_name = "未知身份"
            id_number = "未知身份证号"

            # 寻找查看档案按钮
            archive_button = person_row.eles('css:button[title="查看档案"]')

            # 如果找不到查看档案按钮，则不进一步查询
            if len(archive_button) == 0:
                log('该记录不存在档案')
            # 如果找到查看档案按钮，则进入档案页进一步查询
            else:
                # 进入档案页
                log('存在档案，开始进一步检查')
                archive_button[0].click()
                time.sleep(1)
                person_name_elements = page.eles('.ellipsis')
                time.sleep(4)
                # 如果获取不到人员姓名，则不进一步判断人员姓名的内容
                if len(person_name_elements) == 0:
                    log("未能获取人员姓名", "WARNING")
                # 如果获取到人员姓名，则进一步判断人员姓名的内容
                else:
                    person_name = person_name_elements[0].text
                    log(f"获取到姓名: {person_name}")
                    # 如果人员姓名不为未知身份，则进一步获取身份证号
                    if person_name != '未知身份':
                        try:
                            id_number = page.ele('text=身份证号').parent().text[4:]
                            log(f"获取到身份证号: {id_number}", "DEBUG")
                        except Exception as e:
                            log(f"获取身份证号失败: {e}", "WARNING")
                    # 如果人员姓名为未知身份，则不获取身份证号
                    else:
                        pass

                # 回到特征搜索标签页
                element = page.ele('css=span.sort-handle[title="特征搜索"]')
                element.click()

                # 关闭人员标签页
                log('正在清理标签页...')
                while True:
                    try:
                        element = page.ele('.lidaicon-h-more-vertical btn-icon-more')
                        element.click()
                        time.sleep(2)
                        element = page.ele('关闭其他应用')
                        element.click()
                        break
                    except Exception as e:
                        log(f'关闭档案窗口失败，重试: {e}', "WARNING")
            """END：获取姓名与身份证号""" 

            # 重命名图片
            log('正在生成规范命名的图片文件...')
            image_name = '{}_{}_{}_{}.png'.format(place_name, time_str, id_number, person_name)
            if os.path.exists(image_name):
                os.remove(image_name)
            os.rename(image_path, image_name)
            log(f'图片已保存为: {image_name}')
            
            # 读取图片内容并yield结果
            with open(image_name, 'rb') as f:
                image_content = f.read()

            log(f'正在向主程序返回抓拍结果: {person_name}')
            
            yield {
                "status": "success",
                "image_name": image_name,
                "image_content": image_content,
                "location": place_name,
                "time": time_str,
                "name": person_name,
                "id_number": id_number
            }

            # 删除图片
            if os.path.exists(image_name):
                os.remove(image_name)

        # 翻页处理
        next_page_button = page.ele('.btn-next')
        if next_page_button and next_page_button.attr('disabled') is None:
            log('处理下一页数据...')
            next_page_button.click()
            time.sleep(5)
        else:
            log('所有页面处理完毕')
            break


def main():
    # 示例：搜索 2026年1月3日 00:00:00 到 23:59:59
    # for result in spider_run('20260103000000', '20260103235959', '凤瑞路七峰大道东南角向北'):
    for result in spider_run('20260202000000', '20260209235959', '工业路与新华路', headless=False):
        print(f"Found violation: {result['name']} at {result['location']}")


if __name__ == '__main__':
    from DrissionPage import Chromium
    browser = Chromium(9222)
    tab = browser.latest_tab
    print(tab.title)
    main()

