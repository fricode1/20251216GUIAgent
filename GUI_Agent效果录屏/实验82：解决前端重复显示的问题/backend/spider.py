from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
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


def spider_one_page(page, engine):
    # 找到person row
    persons = page.eles('.el-table__row ') + page.eles('.el-table__row current-row') + page.eles('.el-table__row')
    print('共{}个人员'.format(len(persons)))
    for person_idx, person_row in enumerate(persons):
        print('-----------行人{}------------'.format(person_idx + 1))
        print(person_row.text)

        archive_button = person_row.eles('css:button[title="查看档案"]')
        if len(archive_button) == 0:
            print('不存在档案')
            continue
        else:
            print('存在档案')

        # 判断是否被抓拍
        person_row.click()
        time.sleep(3)
        img_element = page.ele('xpath=//img[@class="iu-img-view__img"]')  # 定位到图片元素
        src = img_element.attr('src')  # 获取 src 属性
        print(src)
        image_path = '{}.png'.format(person_idx + 1)
        if os.path.exists(image_path):
            os.remove(image_path)
        page.download(src, verify=False, rename=image_path)
        is_caught = ocr_image(image_path, engine)
        if not is_caught:
            print('未被抓拍')
            continue
        else:
            print('被抓拍')

        # 获取抓拍地点和时间
        place_name = '未知地点'
        place_element = person_row.ele('css=td.el-table_1_column_3 .cell .plate span')
        if place_element:
            place_name = place_element.text
            place_name = re.sub(r'\s+', '', place_name)  # 如果不这么写，有空格，windows不支持
        time_str = '19900118092016'
        time_element = person_row.ele('css=td.el-table_1_column_2 .cell .plate span')
        if time_element:
            time_str = time_element.text
            time_str = re.sub(r'\D+', '', time_str)  # 如果不这么写，有空格，windows不支持

        # 进入档案页
        archive_button[0].click()
        time.sleep(1)
        person_name_elements = page.eles('.ellipsis')
        time.sleep(4)  # 等待人员档案页面加载完成
        if len(person_name_elements) == 0:
            print("不存在姓名")
            continue

        person_name = person_name_elements[0].text
        print(person_name)
        id_number = "未知身份证号"
        if person_name != '未知身份':
            # 获取身份证号
            # 定位到 form-wrap 容器
            form_wrap = page.ele('xpath=//div[@class="form-wrap"]')

            # 在 form-wrap 中查找身份证号的值
            id_number_element = form_wrap.ele(
                'xpath=.//span[text()="身份证号"]/following-sibling::span[@class="form-value"]')

            # 提取身份证号（可选择提取 text 或 title 属性）
            if id_number_element:
                id_number = id_number_element.attr('title') or id_number_element.text
                # 打印结果
                print("身份证号：", id_number)

            # 重命名图片
            image_name = '{}_{}_{}_{}.png'.format(place_name, time_str, id_number, person_name)
            if os.path.exists(image_name):
                os.remove(image_name)
            os.rename(image_path, image_name)
            
            # Yield result for integration
            with open(image_name, 'rb') as f:
                image_content = f.read()
            
            yield {
                "status": "success",
                "image_name": image_name,
                "image_content": image_content,
                "location": place_name,
                "time": time_str,
                "name": person_name,
                "id_number": id_number
            }

        # 回到特征搜索标签页
        element = page.ele('css=span.sort-handle[title="特征搜索"]')
        element.click()

        # 关闭人员标签页
        while True:
            try:
                element = page.ele('.lidaicon-h-more-vertical btn-icon-more')  # 右侧的三个点
                element.click()
                time.sleep(2)
                element = page.ele('关闭其他应用')
                element.click()
                break
            except Exception as e:
                print('关闭档案窗口失败，重试', e)


def spider_pages(page, engine):  # 处理翻页逻辑
    while True:
        '''1. 处理当前页面'''
        yield from spider_one_page(page, engine)

        '''2. 翻页'''
        next_page_button = page.ele('.btn-next')
        if next_page_button and next_page_button.attr('disabled') is None:
            print('处理下一页')
            next_page_button.click()
            time.sleep(5)  # 必须等待下一页加载完成
        else:
            print('所有页面分析完成')
            break


def set_place(page, place_str):
    """
    place_str: '凤瑞路七峰大道东南角向北'
    """
    print('开始设置地点')
    page.ele('.el-input__icon h-icon-arrow_right').click()

    while True:
        try:
            time.sleep(2)
            page.ele('.el-input--width el-input el-input--suffix').click().input(place_str)  # 这是动态元素，前面需要等待
            page.ele('.el-input__icon h-icon-search').click()
            break
        except Exception as e:
            print("等待“选择点位”动态元素加载", e)

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
    print('完成设置地点')


def spider_one_day(data_str, place_str, page, engine):
    """
    对某个日期进行爬取
    data_str: '2026/01/02'
    """
    print(page.title)
    page.ele('text= 特征搜索 ').click()
    print('进入特征搜索')

    start_time = data_str + ' 00:00:00'

    # 设置地点
    set_place(page, place_str)

    # 设置开始时间
    element = page.ele('css:input[placeholder="开始时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(start_time)

    # 设置结束时间
    end_time = data_str + ' 23:59:59'
    element = page.ele('css:input[placeholder="结束时间"]')
    element.click()
    element.run_js('this.select();')
    element.input(end_time)

    # 点击查询按钮
    element = page.ele('.el-button primary_search-but el-button--primary')
    element.click()
    time.sleep(10)

    # 点击 表格模式 按钮
    print('开始点击“表格模式”按钮')
    try:
        page.ele('text= 表格模式 ').click()
    except Exception as e:
        page.get_screenshot()
        print(e)
        return
    time.sleep(1)

    # 点击 右侧详情 按钮
    page.ele('text= 右侧详情 ').click()
    time.sleep(1)

    # 遍历查询结果
    yield from spider_pages(page, engine)


def login():
    print('开始登录')
    co = ChromiumOptions()
    # co.headless()
    co.ignore_certificate_errors()
    co.set_argument('--ignore-certificate-errors')
    co.set_argument('--ignore-ssl-errors')

    # co = ChromiumOptions().ignore_certificate_errors().headless(True)
    login_page = ChromiumPage(addr_or_opts=co)
    print('开始进入登录页面')
    login_page.get('https://62.168.12.20:8443/')
    time.sleep(1)
    print(login_page.title)
    if login_page.title == '62.168.12.20:8443':
        login_page.ele('.form-cut-item-username').ele('.el-input__inner').input('370982199305061831')
        login_page.ele('.form-cut-item-password').ele('.el-input__inner').input('Abc@123456')
        wait_time = 15
        print('已经输入用户名和密码，正在等待{}秒'.format(wait_time))
        for i in range(wait_time):
            print(i+1)
            time.sleep(1)
        # 必须等待，否则点击登录按钮没反应
        login_page.ele('.form-cut-item-btn').focus().click()
        print('已经点击登录按钮')
        time.sleep(3)

    if '62.168.12.20' == login_page.title:
        print('成功登录')
    else:
        print('未能成功登录')
        print(login_page.title)
        exit(0)

    print('进入视综平台')
    time.sleep(1)
    while True:
        try:
            time.sleep(2)
            login_page.ele('text=公共安全视频监控共享平台').click()
            print('已经进入视频综合图像平台')
            break
        except Exception as e:
            print('未能进入，报错信息为：{}。当前页面内容为：{}'.format(e, login_page.text))


    time.sleep(4)

    tabs = login_page.get_tabs()
    print('已经打开的标签页如下：')
    for tab in tabs:
        print(tab.title)
        if tab.title == '视频图像综合应用平台':
            return tab
    print('未能打开')
    exit(0)


def spider_one_day_dummy(data_str, place_str, page=None, engine=None):
    """
    生成假数据用于测试（当spider仅能在内网访问时使用）
    data_str: '2026/01/02' (格式化后的日期)
    place_str: 地点字符串
    """
    import random
    import datetime
    
    # 读取示例图片
    example_image_path = 'example.jpg'
    if not os.path.exists(example_image_path):
        print(f"警告：示例图片 {example_image_path} 不存在")
        return
    
    with open(example_image_path, 'rb') as f:
        image_content = f.read()
    
    # 姓氏和名字库
    surnames = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗']
    given_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞', '平', '刚', '桂英']
    
    # 无限循环生成数据
    index = 0
    while True:
        # 随机生成姓名
        surname = random.choice(surnames)
        given_name = random.choice(given_names)
        person_name = surname + given_name
        
        # 随机生成身份证号（370982开头 + 随机出生日期 + 随机序号 + 校验码）
        # 出生年份：1980-2000
        birth_year = random.randint(1980, 2000)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # 简化处理，避免日期无效
        sequence = random.randint(1, 999)
        
        # 身份证前17位
        id_prefix = f"370982{birth_year:04d}{birth_month:02d}{birth_day:02d}{sequence:03d}"
        
        # 计算校验码（简化版本，使用随机）
        check_codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']
        check_code = random.choice(check_codes)
        id_number = id_prefix + check_code
        
        # 生成递增的时间戳
        base_time = datetime.datetime.strptime(data_str, "%Y/%m/%d")
        time_offset = datetime.timedelta(hours=index // 12, minutes=(index % 12) * 5)
        current_time = base_time + time_offset
        time_str = current_time.strftime("%Y%m%d%H%M%S")
        
        image_name = '{}_{}_{}_{}.png'.format(
            place_str,
            time_str,
            id_number,
            person_name
        )
        
        yield {
            "status": "success",
            "image_name": image_name,
            "image_content": image_content,
            "location": place_str,
            "time": time_str,
            "name": person_name,
            "id_number": id_number
        }
        
        # 每5秒yield一次
        time.sleep(5)
        index += 1


def main():
    engine = RapidOCR()
    main_tab = login()
    for result in spider_one_day('2026/01/03', '凤瑞路七峰大道东南角向北', main_tab, engine):
        print(f"Found violation: {result['name']} at {result['location']}")


if __name__ == '__main__':
    main()

