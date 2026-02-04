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

tab.actions.click('.icon icon-date')  # 目的是让日历消失。否则不能点中查询按钮

tab.actions.type(Keys.CTRL_A)
tab.actions.type('2026-02-09')

ele = tab.ele('#search_one')  # 人眼能看见这个元素时，点击这个元素才有效。所以必须之前要先点击一下日历图标，让日历消失。

tab.actions.move_to(ele_or_loc=ele)
tab.actions.click(ele)

# 切换到新标签页

tab = Chromium().latest_tab

trains = tab.eles('css:tr[bed_level_info]')

for train in trains:
    print('--------------------')
    print('软座：', train.ele('css:[id^="RZ_"]').text)
    print('硬卧：', train.ele('css:[id^="YW_"]').text)
    print('软卧：', train.ele('css:[id^="RW_"]').text)