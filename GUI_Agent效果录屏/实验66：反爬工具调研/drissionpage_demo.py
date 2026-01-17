from DrissionPage import Chromium
tab = Chromium().latest_tab
tab.get('https://www.zhihu.com/collection/38887091')
links = tab.eles('.title project-namespace-path')