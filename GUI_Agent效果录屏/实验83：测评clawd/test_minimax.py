import anthropic

# 直接在这里配置，避免环境变量失效
client = anthropic.Anthropic(
    api_key="sk-api-o-Z1yUOhoFmhmLlbcp_0pS1Oe2TjGEzUnp9abyDCctFaKjpVCb-mOYjvCzkV9y3APaNmY3wxLM5ho8kkVfGCsrHko5HeduTTZiKW3uZH_Dw0luHNa0MNVOY",
    base_url="https://api.minimax.io/anthropic" 
)

try:
    message = client.messages.create(
        model="MiniMax-M2.1",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "你好，这是一条测试消息。"}
        ]
    )
    print("✅ 请求成功！")
    print("回复内容:", message.content[0].text)
except Exception as e:
    print("❌ 请求失败：")
    print(e)