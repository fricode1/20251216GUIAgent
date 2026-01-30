打开浏览器：
```python
from DrissionPage import Chromium
browser = Chromium()
tab = browser.latest_tab
```

进入登录页：tab.get('https://62.168.12.20:8443/', retry=1, timeout=4) # 若无法连接，则会返回False

这时会出现两种可能。一种是会直接跳转到【应用市场页】 http://62.168.12.20/#/home，这说明已经登录成功。否则，就需要登录：

- 在登录页输入用户名：tab.ele('.form-cut-item-username').ele('.el-input__inner').input('370982199305061831')

- 在登录页输入密码：tab.ele('.form-cut-item-password').ele('.el-input__inner').input('Abc@123456')

- 在登陆页属于用户名和密码后，等待15秒，点击登录按钮：tab.ele('.form-cut-item-btn').focus().click() 成功登录，进入【应用市场页】

在【应用市场页】，点击公共安全视频监控平台按钮： tab.ele('text=公共安全视频监控共享平台').click() 弹出视综平台标签页

切换到视综平台标签页：time.sleep(5); tab = browser.latest_tab; time.sleep(3);

在视综平台，点击身份确认按钮：tab.eles('身份确认')[1].click() 进入身份确认页面

在身份确认页面输入姓名：tab.ele('@placeholder=请输入精确姓名').click().input('张三丰')

在身份确认页面，输入姓名后，点击查询按钮：tab.ele(' 查询 ').click() 获取所有该姓名的人的卡片

在身份确认页面，输入姓名后，点击查询按钮后，获取所有卡片：tab.eles('@class:basic-wrap id-l-content__card hover')

对于每个人的卡片，获取图像：person_card.ele('tag:img')

对于每个人的卡片，获取行人： person_card.ele('@class:text-ellipsis').text

对于每个人的卡片，获取身份证号：person_card.ele('@class:text_certificateNumber').text

## 不得使用的错误语法

tab.wait(timeout=3) - 这么写是错误的，TypeError: OriginWaiter.__call__() got an unexpected keyword argument 'timeout'. 应该用 time.sleep(3)