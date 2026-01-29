from DrissionPage import Chromium
import time
import csv

def scrape_zhihu_collection(url):
    # 1. 初始化浏览器
    browser = Chromium()
    tab = browser.latest_tab
    tab.get(url)
    
    data_list = []

    while True:
        print(f"正在处理页面: {tab.url}")
        
        # 2. 获取当前页面所有内容卡片
        # 使用 tab.eles 获取列表
        cards = tab.eles('.CollectionDetailPageItem-innerContainer')
        print('内容数量：', len(cards))
        
        for card in cards:
            # --- 在每个卡片作用域内查找元素，注意使用 card.ele 而不是 tab.ele ---

            # 获取标题
            title_ele = card.ele('@data-za-detail-view-element_name=Title')
            title = title_ele.text if title_ele else "无标题"

            # 查找“阅读全文”按钮
            # timeout=1 表示如果1秒内没找到（说明已经是全文），则跳过
            expand_btn = card.ele('text=阅读全文', timeout=1)

            if expand_btn:
                expand_btn.click()
                # 点击后稍微等待内容加载（知乎会有个小动画或请求）
                tab.wait(0.5, 1)

            # 获取全文内容
            content_ele = card.ele('.RichContent-inner')
            content = content_ele.text if content_ele else ""

            # 收起内容（可选，为了保持页面整洁，防止遮挡下一条）
            # collapse_btn = card.ele('text=收起', timeout=1)
            # if collapse_btn:
            #     collapse_btn.click()

            print(f"成功抓取: {title[:20]}...")
            data_list.append({
                '标题': title,
                '内容': content
            })

        # 3. 翻页逻辑
        next_btn = tab.ele('text=下一页', timeout=2)
        if next_btn:
            # 判断按钮是否可用（有些页面最后一页也有“下一页”但不可点击）
            if next_btn.link or 'disabled' not in next_btn.attrs.get('class', ''):
                next_btn.click()
                tab.wait.load_start() # 等待新页面加载完毕
                time.sleep(2) # 强制等待，防止知乎频率限制
            else:
                print("已到达最后一页")
                break
        else:
            print("未找到下一页按钮，结束抓取")
            break

    # 4. 保存数据
    save_to_csv(data_list)
    browser.quit()

def save_to_csv(data):
    if not data: return
    with open('zhihu_collection.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['标题', '内容'])
        writer.writeheader()
        writer.writerows(data)
    print(f"总计抓取 {len(data)} 条数据，已保存至 zhihu_collection.csv")

if __name__ == '__main__':
    collection_url = 'https://www.zhihu.com/collection/19928423'
    scrape_zhihu_collection(collection_url)