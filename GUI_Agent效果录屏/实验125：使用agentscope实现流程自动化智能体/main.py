# -*- coding: utf-8 -*-
"""
流程自动化智能体系统
====================

根据用户输入的任务，自动路由到对应的业务系统和执行方式：
- 视综业务系统 (script): 交通违章、监控查询、道路行人违法等 → Python脚本
- 自有业务系统 (api): 渣土车、车辆布控、预警等 → API调用
- 其他业务系统 (gui): 购买火车票、外部网站等 → 视觉GUI Agent
"""
import asyncio
import json
import os
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import OpenAIChatModel

# DeepSeek 配置
api_key = "sk-588ceaf7b0f542f8881fb62161e9127c"
model_name = "deepseek-chat"
base_url = "https://api.deepseek.com"


class TaskType(str, Enum):
    """任务类型枚举"""
    SCRIPT = "script"  # Python脚本执行
    API = "api"       # API调用
    GUI = "gui"       # 视觉GUI操作


class SystemType(str, Enum):
    """业务系统枚举"""
    VIDEO = "视综业务系统"        # 视综业务系统
    OWN = "自有业务系统"          # 自有业务系统
    OTHER = "其他业务系统"        # 其他业务系统


class RoutingResult(BaseModel):
    """路由结果模型"""
    task_type: TaskType = Field(description="任务执行方式: script/api/gui")
    system: SystemType = Field(description="业务系统类型")
    desc: str = Field(description="任务说明")


# ============================================================
# 创建各个执行 Agent
# ============================================================

def create_model():
    """创建通用模型配置"""
    return OpenAIChatModel(
        model_name=model_name,
        api_key=api_key,
        client_kwargs={"base_url": base_url},
    )


def create_script_agent() -> ReActAgent:
    """创建脚本执行 Agent - 处理视综业务系统的Python脚本执行"""
    return ReActAgent(
        name="脚本执行Agent",
        sys_prompt="""你是一个流程自动化脚本执行专家。

你的职责是执行视综业务系统的Python脚本任务。

常见任务包括：
- 查询交通违章记录（如：新华路今天的行人违章）
- 监控视频相关操作
- 道路行人违法检测

请根据用户需求，生成并执行相应的Python脚本来完成任务。
记住你是在处理【视综业务系统】相关的任务。""",
        model=create_model(),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
    )


def create_api_agent() -> ReActAgent:
    """创建API调用 Agent - 处理自有业务系统的API调用"""
    return ReActAgent(
        name="API调用Agent",
        sys_prompt="""你是一个API调用专家。

你的职责是调用自有业务系统的API来完成车辆布控任务。

常见任务包括：
- 对渣土车进行布控
- 车辆预警管理
- 布控任务创建、查询、删除

请根据用户需求，调用相应的API接口完成任务。
记住你是在处理【自有业务系统】相关的API调用任务。""",
        model=create_model(),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
    )


def create_gui_agent() -> ReActAgent:
    """创建视觉GUI Agent - 处理第三方系统的视觉交互操作"""
    return ReActAgent(
        name="视觉GUIAgent",
        sys_prompt="""你是一个视觉GUI操作专家。

你的职责是使用Midscene等视觉交互引擎来操作第三方系统。

常见任务包括：
- 购买火车票（12306网站）
- 操作外部网站
- 执行需要GUI交互的任务

请根据用户需求，使用视觉AI能力来模拟用户操作GUI界面完成任务。
记住你是在处理【其他业务系统】的GUI交互任务。""",
        model=create_model(),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
    )


# ============================================================
# 任务路由 Agent
# ============================================================

def create_router_agent() -> ReActAgent:
    """创建任务路由 Agent - 核心大脑，判断业务系统和执行方式"""
    return ReActAgent(
        name="任务路由Agent",
        sys_prompt="""你是一个智能任务路由专家。

请根据用户输入的任务，自动匹配对应的【业务系统】和【执行方式】，严格按下面规则：

--- 规则 ---
1. 任务内容包含：交通违章、监控查询、道路行人违法、视综平台
   → 业务系统：视综业务系统
   → 执行方式：script（Python脚本）

2. 任务内容包含：渣土车、车辆布控、预警、布控任务、自有平台、内部系统
   → 业务系统：自有业务系统
   → 执行方式：api（API调用）

3. 任务内容包含：购买火车票、12306、外部网站、第三方GUI操作
   → 业务系统：其他业务系统
   → 执行方式：gui（视觉GUI Agent）

--- 输出要求 ---
只返回JSON，不要任何多余解释，格式如下：
{
  "task_type": "script/api/gui",
  "system": "视综业务系统/自有业务系统/其他业务系统",
  "desc": "任务说明"
}
""",
        model=create_model(),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
    )


# ============================================================
# 主程序
# ============================================================

async def route_and_execute(user_input: str) -> str:
    """路由并执行任务

    Args:
        user_input: 用户输入的任务描述

    Returns:
        执行结果
    """
    # 1. 创建路由 Agent
    print('创建路由agent')
    router = create_router_agent()

    # 2. 获取路由结果
    print("获取路由结果")
    msg_user = Msg(name="user", content=user_input, role="user")
    msg_response = await router(msg_user, structured_model=RoutingResult)

    # 3. 解析路由结果
    print("解析路由结果")
    routing_info = msg_response.metadata
    task_type = routing_info.get("task_type")
    system = routing_info.get("system")
    desc = routing_info.get("desc", user_input)

    print(f"\n{'='*50}")
    print(f"📋 路由结果")
    print(f"{'='*50}")
    print(f"  系统: {system}")
    print(f"  方式: {task_type}")
    print(f"  描述: {desc}")
    print(f"{'='*50}\n")

    # 4. 根据路由结果分发到对应的执行 Agent
    if task_type == "script":
        print("🔄 正在路由到 [脚本执行Agent]...")
        agent = create_script_agent()
        result = await agent(Msg(name="user", content=desc, role="user"))
        return result.content

    elif task_type == "api":
        print("🔄 正在路由到 [API调用Agent]...")
        agent = create_api_agent()
        result = await agent(Msg(name="user", content=desc, role="user"))
        return result.content

    elif task_type == "gui":
        print("🔄 正在路由到 [视觉GUIAgent]...")
        agent = create_gui_agent()
        result = await agent(Msg(name="user", content=desc, role="user"))
        return result.content

    else:
        return f"❌ 无法识别的任务类型: {task_type}"


async def main():
    """主程序入口"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         🚀 流程自动化智能体系统 v1.0                      ║
║                                                          ║
║   支持以下业务系统的任务自动路由与执行:                    ║
║   - 视综业务系统 (Python脚本)                              ║
║   - 自有业务系统 (API调用)                                 ║
║   - 其他业务系统 (视觉GUI操作)                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    # 示例任务
    example_tasks = [
        "查询新华路今天的行人违章",
        "对渣土车进行布控",
        "购买明天去北京的高铁票",
    ]

    print("📝 示例任务:")
    for i, task in enumerate(example_tasks, 1):
        print(f"   {i}. {task}")
    print()

    # 交互式输入
    while True:
        try:
            user_input = input("💬 请输入任务（输入 'quit' 退出）: ").strip()
            if user_input.lower() == 'quit':
                print("👋 再见!")
                break
            if not user_input:
                continue

            result = await route_and_execute(user_input)
            print(f"\n📤 执行结果:\n{result}\n")

        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"\n❌ 执行出错: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
