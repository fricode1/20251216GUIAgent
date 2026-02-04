from DrissionPage import Chromium
tab = Chromium().latest_tab

trains = tab.eles('css:tr[bed_level_info]')

for train in trains:
    硬卧余票 = train.ele('css:[id^="YW_"]').text
    if 硬卧余票 != '--':
        print('有票')
        预订按钮 = train.ele('预订').click()

