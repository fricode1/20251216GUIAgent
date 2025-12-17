import asyncio
from agent import ComputerAgent
from computer import Computer
import os
import time
# os.environ["CUA_API_KEY"] = "sk_cua-api01_5e6672b37c301fd7c107211151629dd666b8061f491fdedb0fe2eecf1aaca247"
os.environ["OPENROUTER_API_KEY"] = "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"
async def main():
    # 1. 初始化电脑连接 (连接到本地)
    computer = Computer(
        os_type="windows",  # or "macos", "linux"
        use_host_computer_server=True
    )

    # 2. 初始化 Agent
    # 注意：使用 anthropic 模型需要设置环境变量 ANTHROPIC_API_KEY
    agent = ComputerAgent(
        # model="cua/bytedance/ui-tars-2",
        model="openrouter/z-ai/glm-4.5v",
        tools=[computer],
        max_trajectory_budget=5.0
    )

    messages = [{"role": "user", "content": "在右侧已打开的浏览器中，进入百度百科并搜索电视剧《武林外传》词条"}]

    start = time.time()
    try:
        # 3. 建立连接
        await computer.run()
        print("已连接到本地电脑，Agent 开始思考...")

        # 4. 运行 Agent (必须在 async 函数内)
        async for result in agent.run(messages):
            if "output" in result:
                for item in result["output"]:
                    # 打印 AI 的回复
                    if item.get("type") == "message":
                        print("AI:", item["content"][0]["text"])
                    # 打印 AI 的思考过程 (可选)
                    elif item.get("type") == "reasoning":
                        print("Thinking:", item.get("summary", [{}])[0].get("text", "..."))

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 5. 关闭连接
        await computer.stop()
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    # 启动异步主程序
    asyncio.run(main())