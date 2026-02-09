import os
from DrissionPage import ChromiumPage

def launch_target_page():
    # 获取本地 target_page.html 的绝对路径
    file_path = os.path.abspath('target_page.html')
    url = f'file://{file_path}'
    
    # 启动浏览器并访问页面
    page = ChromiumPage()
    page.get(url)
    print(f"已启动浏览器并访问: {url}")
    
    # 保持运行以便观察，实际使用中可以根据需要调整
    input("按下回车键关闭浏览器并退出程序...")
    page.quit()

if __name__ == "__main__":
    launch_target_page()
