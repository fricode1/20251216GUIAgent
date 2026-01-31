# 讯飞开放平台 - 在线语音合成：收费版最低2000元/年
#  https://www.xfyun.cn/services/online_tts?target=price

# 百度：已经充值21元

import requests

API_KEY = "Jfs4UJ1WfADMODPtIR8J0gnW"
SECRET_KEY = "JbFZGhrjmCQ2RnXv3gcluIxAqMOfdfGZ"

def main():
        
    url = "https://tsn.baidu.com/text2audio"
    
    payload='tex=%E4%BD%A0%E5%A5%BD&tok='+ get_access_token() +'&cuid=DQDvyz13icXAcC1CgVv9wNVlD7KGYM9r&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=4194&aue=3'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'cuid': '0UeoCxtDtPWjxsoaztkir2BIuiNBFEic'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    # --- 关键部分：处理返回结果 ---
    
    # 检查返回的内容类型
    content_type = response.headers.get('Content-Type')
    
    if content_type == 'audio/mp3' or 'audio' in content_type:
        # 如果返回的是音频流，则保存为文件
        file_name = "output.mp3"
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"合成成功，音频已保存为: {file_name}")
    else:
        # 如果返回的是 application/json，说明出错了
        print("合成失败，错误信息：")
        print(response.json())
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
