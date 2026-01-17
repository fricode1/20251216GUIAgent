*** Settings ***
Library    SeleniumLibrary
Library    RPA.Desktop

*** Variables ***
${URL}            https://www.baidu.com
# Windows 路径在 Robot 中建议使用双反斜杠 \\ 或正斜杠 /
${FILE_PATH}      C:\\Users\\admin\\Pictures\\Default.jpg
# 这里的定位符通过你提供的 SVG 特征进行精准匹配，确保点击的是“回形针”图标
${UPLOAD_BTN}     xpath=//div[contains(@class, 'tool-item')][.//*[local-name()='svg']/*[contains(@d, 'M11.4405')]]

*** Test Cases ***
百度AI输入框文件上传测试
    [Documentation]    点击回形针图标并上传 Default.jpg
    打开百度并等待加载
    触发上传对话框
    处理系统窗口上传文件
    校验上传状态
    [Teardown]    Close Browser

*** Keywords ***
打开百度并等待加载
    # 百度首页目前会自动加载 AI 搜索框
    Open Browser    ${URL}    Chrome
    Maximize Browser Window
    # 等待上传图标出现在页面上（最多等待 15 秒）
    Wait Until Element Is Visible    ${UPLOAD_BTN}    timeout=15s

触发上传对话框
    # 点击那个包含 SVG 的 div 容器
    Click Element    ${UPLOAD_BTN}
    # 关键：必须等待 1.5 秒左右，直到 Windows 的“打开”窗口完全弹出并获得焦点
    Sleep    1.5s

处理系统窗口上传文件
    # RPA.Desktop 会在操作系统层面模拟打字，将路径输入到弹出的文件对话框中
    RPA.Desktop.Type Text    ${FILE_PATH}
    # 模拟按下 Enter 键，相当于点击对话框的“打开”按钮
    RPA.Desktop.Press Keys    enter
    # 给一点上传缓冲时间
    Sleep    3s

校验上传状态
    # 上传成功后，百度 AI 框通常会显示文件名或缩略图
    # 这里可以添加 Wait Until Page Contains 或其他校验逻辑
    Log    文件上传指令已发送