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
from browser_use import ChatOpenAI, sandbox, Browser
import asyncio, os, time


async def my_task():
    # Get API key from https://www.modelscope.cn/docs/model-service/API-Inference/intro
    # os.environ["MODELSCOPE_API_KEY"] = "ms-76ba9907-1588-4484-b2c6-cd18fe67c0ad"  # 不是百炼，是modelscope
    # api_key = os.getenv('MODELSCOPE_API_KEY')
    # base_url = 'https://api-inference.modelscope.cn/v1/'
    # llm = ChatOpenAI(model='Qwen/Qwen3-VL-235B-A22B-Instruct', api_key=api_key, base_url=base_url)

    # 千帆
    # api_key = "bce-v3/ALTAK-WEtfPuAdoIz3APYflYveE/5f92d54547ab2be4834c6f6bc9671e4e1f48f4de"
    # base_url = 'https://qianfan.baidubce.com/v2/'
    # model = "ernie-5.0-thinking-preview"
    # llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

    # 百炼
    api_key = 'sk-efe1c9004f7e4de0a8ade26120301c6d'
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    model = 'qwen-vl-max'
    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

    # 任务
    # task = '1. 进入 https://www.weather.com.cn/ 查询北京天气 2. 将北京天气浓缩成140以内 3. 进入 https://weibo.com/ 点击写微博按钮 4. 发布北京天气'
    task = """
        https://zj.zol.com.cn/ 订制攒机方案

        1. 配置 CPU 主板 内存 硬盘
        当装机配置单中某个设备没有配置时，对应条目会显示“请选择商品”，且该设备各型号产品对应的“加入配置单”按钮为蓝色。
        当装机配置单中某个设备成功配置时，对应条目会显示具体型号产品，且被添加的产品对应的“加入配置单”按钮为灰色。
        当装机配置单中某个设备成功配置后，进行下一个设备的配置，不能重复配置同一设备。切勿点击已变成灰色的“加入配置单”按钮。

        2. 上述四个硬件配置完成后，在 名称 文本框 输入 我的装机配置清单

        3. 点击预览按钮。点击预览按钮后立即结束所有操作。
        """

    # 设置浏览器（记住登录信息）
    executable_path='/usr/bin/google-chrome'
    user_data_dir='~/.config/google-chrome'

    # Connect to your existing Chrome browser
    browser = Browser(
        executable_path=executable_path,
        user_data_dir=user_data_dir,
        profile_directory='Default',
    )

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

