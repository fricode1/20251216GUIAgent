from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
    # 获取现有的上下文 (Context)
    context = browser.contexts[0]

    # 获取所有已打开的标签页
    pages = context.pages
    page = pages[0]
    
    client = page.context.new_cdp_session(page)
    # 获取完整的无障碍树
    ax_tree = client.send("Accessibility.getFullAXTree")
    
    # ax_tree 包含非常详尽的节点数组，需要根据 parentId 逻辑自行还原
    # 这通常用于非常底层的数据抓取
    print(ax_tree['nodes']) 