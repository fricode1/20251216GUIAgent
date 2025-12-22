import asyncio
from browser_use import Agent, Browser, ChatOpenAI, ChatBrowserUse

llm = ChatBrowserUse(api_key='bu_eWRuVFK-tQu2KV_6JugfZ4vyD2a8qK-UslRhpiIUK5Q')

# Connect to your existing Chrome browser
browser = Browser(
    cdp_url="http://127.0.0.1:9222"  # 替换为实际的 CDP 地址
)

agent = Agent(
    task='Visit https://www.zhihu.com 总结你看到的内容',
    browser=browser,
    llm=llm,
)
async def main():
	await agent.run()

if __name__ == "__main__":
    asyncio.run(main())