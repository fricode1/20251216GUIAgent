from DrissionPage import Chromium
tab = Chromium().latest_tab

trains = tab.eles('css:tr[bed_level_info]')

for train in trains:
    print('--------------------')
    print('软座：', train.ele('css:[id^="RZ_"]').text)
    print('硬卧：', train.ele('css:[id^="YW_"]').text)
    print('软卧：', train.ele('css:[id^="RW_"]').text)

