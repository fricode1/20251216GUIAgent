"""安装与运行
```bash
conda create -n browser_use_py312 python=3.12
conda activate browser_use_py312
pip install browser-use
```
"""

"""运行
conda activate browser_use_py312
cd code/browser_use_example
python my_browser_use.py
"""

"""使用不同模型
https://docs.browser-use.com/supported-models
"""

from browser_use.agent.service import Agent
from browser_use import ChatOpenAI, sandbox
import asyncio, os, time


async def my_task():
    # Get API key from https://www.modelscope.cn/docs/model-service/API-Inference/intro
    #os.environ["MODELSCOPE_API_KEY"] = "ms-76ba9907-1588-4484-b2c6-cd18fe67c0ad"  # 不是百炼，是modelscope
    #api_key = os.getenv('MODELSCOPE_API_KEY')
    #base_url = 'https://api-inference.modelscope.cn/v1/'
    # llm = ChatOpenAI(model='Qwen/Qwen3-VL-235B-A22B-Instruct', api_key=api_key, base_url=base_url)

    # 千帆
    api_key = "bce-v3/ALTAK-WEtfPuAdoIz3APYflYveE/5f92d54547ab2be4834c6f6bc9671e4e1f48f4de"
    base_url = 'https://qianfan.baidubce.com/v2/'
    model = "ernie-5.0-thinking-preview"

    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

    agent = Agent(
        task="介绍百度百科中搜索“武林外传”词条",
        llm=llm,
        use_vision=True
    )
    start = time.time()
    await agent.run()
    end = time.time()
    print(end-start)

# Just call it like any async function
asyncio.run(my_task())

