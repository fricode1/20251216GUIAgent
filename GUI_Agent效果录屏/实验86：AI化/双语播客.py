import requests
from urllib.parse import quote
import os

# 配置你的 Key
API_KEY = "Jfs4UJ1WfADMODPtIR8J0gnW"
SECRET_KEY = "JbFZGhrjmCQ2RnXv3gcluIxAqMOfdfGZ"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    res = requests.post(url, params=params)
    if res.status_code == 200:
        return res.json().get("access_token")
    else:
        print("获取 Token 失败，请检查 API_KEY 和 SECRET_KEY")
        return None

def main():
    # 1. 检查文件是否存在并读取内容
    file_path = "中文.txt"
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text_content = f.read().strip()

    if not text_content:
        print("错误：文件内容为空")
        return

    print(f"正在合成文本，长度：{len(text_content)} 字")

    # 2. 获取 Access Token
    token = get_access_token()
    if not token:
        return

    # 3. 准备请求参数
    url = "https://tsn.baidu.com/text2audio"
    
    # 对文本进行 URL 编码
    tex_encoded = quote(text_content)
    
    # 拼接 payload
    # per: 发音人ID, 4194 是你代码中选用的
    # aue: 3 是 mp3 格式
    payload = (
        f'tex={tex_encoded}'
        f'&tok={token}'
        f'&cuid=DQDvyz13icXAcC1CgVv9wNVlD7KGYM9r'
        f'&ctp=1'
        f'&lan=zh'
        f'&spd=5'
        f'&pit=5'
        f'&vol=5'
        f'&per=4194'
        f'&aue=3'
    )
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }

    # 4. 发送请求
    try:
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        
        # 5. 处理结果
        content_type = response.headers.get('Content-Type')

        if 'audio' in content_type:
            # 如果返回的是音频
            output_file = "output.mp3"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"--- 合成成功 ---")
            print(f"文件已保存为: {os.path.abspath(output_file)}")
        else:
            # 如果返回的是 JSON (说明报错了)
            print("--- 合成失败 ---")
            print(response.json())
            
    except Exception as e:
        print(f"网络请求发生错误: {e}")

if __name__ == '__main__':
    main()