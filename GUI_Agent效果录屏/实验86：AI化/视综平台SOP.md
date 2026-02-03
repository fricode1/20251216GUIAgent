打开浏览器：
```python
from DrissionPage import Chromium
browser = Chromium()
tab = browser.latest_tab
```

进入登录页：tab.get('https://62.168.12.20:8443/', retry=1, timeout=4)

这时会出现三种可能：
（1）若无法连接，则会返回False
（2）成功连接，且直接跳转到【应用市场页】 http://62.168.12.20/#/home，这说明已经登录成功。
（3）否则，就需要登录：

- 在登录页输入用户名：tab.ele('.form-cut-item-username').ele('.el-input__inner').input('370982199305061831')

- 在登录页输入密码：tab.ele('.form-cut-item-password').ele('.el-input__inner').input('Abc@123456')

- 在登陆页属于用户名和密码后，等待15秒，点击登录按钮：tab.ele('.form-cut-item-btn').focus().click() 成功登录，进入【应用市场页】

在【应用市场页】，点击公共安全视频监控平台按钮： tab.ele('text=公共安全视频监控共享平台').click() 弹出视综平台标签页

切换到视综平台标签页：time.sleep(5); tab = browser.latest_tab; time.sleep(3);

在视综平台，点击身份确认按钮：tab.eles('身份确认')[1].click(); time.sleep(5) 进入【身份确认页面】

## 身份确认页面

该页面有多种使用方式：根据图片确认身份、根据姓名确认身份。如果用户提供的是图片，则执行根据图片确认身份而非根据姓名确认身份。如果用户提供的是姓名，则执行根据姓名确认身份而非根据图片确认身份。

### 根据图片确认身份

在身份确认页面上传图像：tab.ele('.el-upload-dragger').click.to_upload('/home/zcc/zhbli/projects/实验86：AI化/face.png')

获取图像对应的身份的姓名：tab.ele('.human-name').wait.enabled().text

获取图像对应的身份的身份证号：tab.ele('.certificate-num').text

### 根据姓名确认身份

在身份确认页面输入姓名：tab.ele('@placeholder=请输入精确姓名').click().input(用户提供的想要查询的姓名)

在身份确认页面，输入姓名后，点击查询按钮：tab.ele(' 查询 ').click() 获取所有该姓名的人的卡片

在身份确认页面，输入姓名后，点击查询按钮后，获取所有卡片：tab.eles('@class:basic-wrap id-l-content__card hover')

对于每个人的卡片，获取图像：person_card.ele('tag:img')

对于每个人的卡片，获取行人： person_card.ele('@class:text-ellipsis').text

对于每个人的卡片，获取身份证号：person_card.ele('@class:text_certificateNumber').text

## 不得使用的错误语法

tab.wait(timeout=3) - 这么写是错误的，TypeError: OriginWaiter.__call__() got an unexpected keyword argument 'timeout'. 应该用 time.sleep(3)