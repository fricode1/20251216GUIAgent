# 通过指定浏览器路径实现记住登录信息的功能
import asyncio
from browser_use import Agent, Browser, ChatOpenAI

executable_path='/usr/bin/google-chrome'
user_data_dir='~/.config/google-chrome'

# Connect to your existing Chrome browser
browser = Browser(
    executable_path=executable_path,
    user_data_dir=user_data_dir,
    profile_directory='Default',
)

agent = Agent(
    task='Visit https://www.zhihu.com',
    browser=browser,
    llm=ChatOpenAI(model='gpt-4.1-mini'),
)
async def main():
	await agent.run()

if __name__ == "__main__":
    asyncio.run(main())