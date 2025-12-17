import asyncio, os
from agent import ComputerAgent
from computer import Computer
os.environ["CUA_API_KEY"] = "sk_cua-api01_5e6672b37c301fd7c107211151629dd666b8061f491fdedb0fe2eecf1aaca247"
async def main():
    computer = Computer(os_type="windows", use_host_computer_server=True)
    agent = ComputerAgent(model="cua/bytedance/ui-tars-2", tools=[computer], max_trajectory_budget=5.0)
    messages = [{"role": "user", "content": "在浏览器中，打开百度百科，搜索词条《武林外传》"}]
    await computer.run()
    async for result in agent.run(messages):
        if "output" in result:
            for item in result["output"]:
                if item.get("type") == "message": print("AI:", item["content"][0]["text"])
    await computer.stop()
if __name__ == "__main__":
    asyncio.run(main())