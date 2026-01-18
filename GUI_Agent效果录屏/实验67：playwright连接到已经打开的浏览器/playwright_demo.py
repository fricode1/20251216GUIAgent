from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
    # 获取现有的上下文 (Context)
    context = browser.contexts[0]

    # 获取所有已打开的标签页
    pages = context.pages
    page = pages[0]
    if len(page.frames) > 1:
        print(f"页面上有 {len(page.frames) - 1} 个 iframe")

    # 1. 创建 CDP 会话
    client = page.context.new_cdp_session(page)
    
    # 2. 执行底层命令获取快照
    snapshot = client.send("Page.captureSnapshot", {"format": "mhtml"})
    
    # 3. 保存内容
    with open("full_page.mhtml", "w", encoding="utf-8") as f:
        f.write(snapshot['data'])
        
    print("已保存为 full_page.mhtml，该文件包含所有 iframe 内容。")