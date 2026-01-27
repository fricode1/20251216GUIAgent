from zai import ZhipuAiClient

# 初始化客户端
client = ZhipuAiClient(api_key="5aab6fda6039467ebe3c011e5935b856.FrUFg7WiNub5cLYp")

# 创建聊天完成请求
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[
        {
            "role": "system",
            "content": "你是一个有用的AI助手。"
        },
        {
            "role": "user",
            "content": "你好，请介绍一下自己。"
        }
    ],
    temperature=0.6
)

# 获取回复
print(response.choices[0].message.content)