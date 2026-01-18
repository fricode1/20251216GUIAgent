from DrissionPage import Chromium

page = Chromium().latest_tab
page.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe')

# 调用 CDP 命令 Page.captureSnapshot 获取全页面快照（MHTML 格式）
# 这包含了主页面和所有 iframe 的加密合并内容
res = page.run_cdp('Page.captureSnapshot', format='mhtml')
mhtml_data = res['data']

with open('full_page.mhtml', 'w', encoding='utf-8') as f:
    f.write(mhtml_data)

print("全页面快照已保存为 .mhtml 格式（可用 Chrome 直接打开）")