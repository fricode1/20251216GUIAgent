"""安装与运行
```bash
conda create -n browser_use_py312 python=3.12
conda activate browser_use_py312
pip install browser-use
```
"""

"""运行
conda activate browser_use_py312
cd /home/zhbli/projects/20251216GUIAgent/GUI_Agent效果录屏/实验27：通过不断优化提示词完成12306订票
python my_browser_use.py
"""

from browser_use.agent.service import Agent
from browser_use import ChatOpenAI, sandbox, Browser
import asyncio, os, time


async def my_task():
    # 百炼
    api_key = 'sk-efe1c9004f7e4de0a8ade26120301c6d'
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    model = 'qwen-vl-max'
    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

    task = """
        1. 进入 12306.cn
        2. 在出发地文本框填入 北京北
        3. 在下拉列表中点击 北京北
        4. 在到达地文本框填入 怀柔北
        5. 在下拉列表中点击 怀柔北
        6. 在出发日期文本框填入 2025-12-31（绝对不要click出发日期文本框，而是直接填入）
        7. 点击查询按钮。
        8. 点击后，12036网站会自动打开一个新的标签页。你要跳转到这个新的标签页进行后续操作。
        9. 点击 4471 次列车的预定按钮
        10. 勾选乘车人 李振邦
        11. 点击 提交订单按钮
        """

    cdp_url = 'ws://127.0.0.1:9222/devtools/browser/6de34a82-8b00-4fd6-a50c-4efc93cc6a09'
    browser = Browser(cdp_url=cdp_url)

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
        browser=browser,
    )
    start = time.time()
    await agent.run()
    end = time.time()
    print(end-start)

# Just call it like any async function
asyncio.run(my_task())

