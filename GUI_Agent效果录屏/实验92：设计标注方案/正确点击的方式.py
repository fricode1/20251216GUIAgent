from DrissionPage import Chromium
tab = Chromium().latest_tab
ele_selector = 'xpath://*[@id="panel_cities"]//*[text()="泰安"]'
tab.actions.click(ele_selector)