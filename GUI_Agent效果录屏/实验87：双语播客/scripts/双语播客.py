import requests
from urllib.parse import quote
import os
import time

# 配置你的 Key
API_KEY = "Jfs4UJ1WfADMODPtIR8J0gnW"
SECRET_KEY = "JbFZGhrjmCQ2RnXv3gcluIxAqMOfdfGZ"

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    res = requests.post(url, params=params)
    if res.status_code == 200:
        return res.json().get("access_token")
    return None

def main():
    file_name = 'Chapter 15'
    file_path = r"C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\各章节\{}.txt".format(file_name)
    output_filename = r"C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\各章节\{}.mp3".format(file_name)
    
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    # 1. 获取 Token
    token = get_access_token()
    if not token:
        print("Token 获取失败")
        return

    # 2. 读取并解析文件
    with open(file_path, "r", encoding="utf-8") as f:
        # 过滤掉空行
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("文件内容为空")
        return

    print(f"检测到 {len(lines)} 段文本，开始分段合成并合并...")

    # 3. 循环请求并将结果写入同一个文件
    # 注意：'wb' 模式打开文件，后续用 'ab' 模式追加
    with open(output_filename, "wb") as final_file:
        for index, text in enumerate(lines):
            print(f"正在合成第 {index+1}/{len(lines)} 段...")
            
            # 这里设置单段合成参数
            url = "https://tsn.baidu.com/text2audio"
            tex_encoded = quote(text)
            
            payload = (
                f'tex={tex_encoded}'
                f'&tok={token}'
                f'&cuid=python_script'
                f'&ctp=1'
                f'&lan=zh'
                f'&spd=5'
                f'&pit=5'
                f'&vol=5'
                f'&per=4194'
                f'&aue=3' # 必须是 mp3 格式
            )
            
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            try:
                response = requests.post(url, headers=headers, data=payload.encode("utf-8"))
                content_type = response.headers.get('Content-Type')

                if 'audio' in content_type:
                    # 将本次返回的二进制音频流直接写入文件末尾
                    final_file.write(response.content)
                else:
                    print(f"第 {index+1} 段合成失败，原因：{response.json()}")
                
                # 稍微停顿一下，防止请求过快
                time.sleep(0.2)

            except Exception as e:
                print(f"处理第 {index+1} 段时发生网络错误: {e}")

    print("-" * 30)
    print(f"所有段落处理完成！")
    print(f"完整音频已保存至: {os.path.abspath(output_filename)}")

if __name__ == '__main__':
    main()