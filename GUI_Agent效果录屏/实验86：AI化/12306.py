from DrissionPage import Chromium
from DrissionPage.common import Keys

Chromium().latest_tab.get('https://www.12306.cn')

tab = Chromium().latest_tab

print('输入出发地')

tab.actions.click('#fromStationText')

tab.actions.type('chongqingbei')  # 必须用type, 不能用 input. 因为 type 能触发 key_up 事件

tab.ele('.citylineover').click()

tab.actions.click('#toStationText')

tab.actions.type(Keys.CTRL_A)  # 必须全选，否则文本会跟在文本框中已有文本的后面

tab.actions.type('chongqingdong')

tab.ele('.citylineover').click()

tab.actions.click('.input-box input-data')

tab.actions.type(Keys.CTRL_A)
tab.actions.type('2026-02-09')

# ele = tab.ele('#search_one')
# print(ele)

# tab.actions.move_to(ele_or_loc=ele)
# tab.actions.click(ele)
