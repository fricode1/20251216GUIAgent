from DrissionPage import Chromium
tab = Chromium().latest_tab

trains = tab.eles('css:tr[bed_level_info]')

for train in trains:
    硬卧余票 = train.ele('css:[id^="YW_"]').text
    if 硬卧余票 != '--':
        print('有票')
        预订按钮 = train.ele('预订').click()

        # 弹出登录界面
        try:
            登录框 = tab.ele('.input')
            登录框.input('13260295020')

            密码框 = tab.ele('.login-item')
            input('完成登录后，按任意键')
        except Exception as e:
            print('已经登录')
            pass

        tab = Chromium().latest_tab
        提交订单按钮 = tab.ele('提交订单')
        确认提交 = input('确认提交订单吗？y/n')
        if 确认提交 == 'y':
            提交订单按钮.click()
        else:
            print(提交订单按钮)
            print('暂不提交')
            exit(0)
        

