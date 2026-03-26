# -*- coding: utf-8 -*-
"""
流程自动化智能体系统
====================

根据用户输入的任务，自动路由到对应的业务系统和执行方式：
- 视综业务系统 (script): 交通违章、监控查询、道路行人违法等 → Python脚本 + API调用
- 自有业务系统 (api): 渣土车、车辆布控、预警等 → API调用
- 其他业务系统 (gui): 购买火车票、外部网站等 → 视觉GUI Agent
"""
import asyncio
import json
import os
from enum import Enum
from typing import Literal, Optional

import requests
from pydantic import BaseModel, Field

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import OpenAIChatModel
from agentscope.tool import Toolkit, ToolResponse

# DeepSeek 配置
api_key = "sk-588ceaf7b0f542f8881fb62161e9127c"
model_name = "deepseek-chat"
base_url = "https://api.deepseek.com"


# ============================================================
# 视综业务系统 API 配置
# ============================================================
VIDEO_SYSTEM_CONFIG = {
    "base_url": "https://62.168.243.10:19080",
    "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA",
}


# ============================================================
# 视综业务系统 API 工具函数
# ============================================================

def list_video_deploy_tasks() -> dict:
    """列出所有布控任务

    Returns:
        所有布控任务的列表
    """
    url = f"{VIDEO_SYSTEM_CONFIG['base_url']}/mrag/api/deploy/tasks/list"
    headers = {"Authorization": VIDEO_SYSTEM_CONFIG["authorization"]}

    response = requests.get(url, headers=headers)
    return response.json()


def create_video_deploy_task(
    name: str,
    target_type: str = "person",
    desc: str = "",
    text: str = "",
    prompt: str = "",
    device_id: str = "",
    start_time: str = "",
    end_time: str = "",
    distance: float = 0.8,
) -> dict:
    """创建布控任务

    Args:
        name: 任务名称
        target_type: 目标类型 (person/vehicle)
        desc: 任务描述
        text: 目标描述文本
        prompt: AI分析提示词
        device_id: 监控设备ID
        start_time: 开始时间 (格式: YYYY-MM-DD HH:MM:SS)
        end_time: 结束时间 (格式: YYYY-MM-DD HH:MM:SS)
        distance: 相似度阈值 (0-1)

    Returns:
        创建结果
    """
    url = f"{VIDEO_SYSTEM_CONFIG['base_url']}/mrag/api/deploy/tasks/create"
    headers = {
        "Authorization": VIDEO_SYSTEM_CONFIG["authorization"],
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "target_type": target_type,
        "desc": desc,
        "deploy_type": 0,
        "image_base64": "",
        "space_time_list": [
            {
                "device_id": device_id,
                "start_time": start_time,
                "end_time": end_time,
                "time_slot_list": []
            }
        ],
        "text": text,
        "distance": distance,
        "prompt": prompt,
        "prompt_image_base64_list": []
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def start_video_deploy_task(task_id: str) -> dict:
    """启动布控任务

    Args:
        task_id: 任务ID

    Returns:
        启动结果
    """
    url = f"{VIDEO_SYSTEM_CONFIG['base_url']}/mrag/api/deploy/tasks/start"
    headers = {
        "Authorization": VIDEO_SYSTEM_CONFIG["authorization"],
        "Content-Type": "application/json"
    }
    payload = {"id": task_id}

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def get_video_deploy_results(task_id: str, page_no: int = 1, page_size: int = 10) -> dict:
    """查看布控结果

    Args:
        task_id: 任务ID
        page_no: 页码
        page_size: 每页数量

    Returns:
        布控结果列表
    """
    url = f"{VIDEO_SYSTEM_CONFIG['base_url']}/mrag/api/deploy/alarm/list"
    headers = {"Authorization": VIDEO_SYSTEM_CONFIG["authorization"]}
    params = {"id": task_id, "pageNo": page_no, "pageSize": page_size}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


# ============================================================
# 视综业务系统工具注册
# ============================================================

def create_video_system_toolkit() -> Toolkit:
    """创建视综业务系统的工具集"""
    toolkit = Toolkit()

    # 注册工具函数
    toolkit.register_tool_function(list_video_deploy_tasks)
    toolkit.register_tool_function(create_video_deploy_task)
    toolkit.register_tool_function(start_video_deploy_task)
    toolkit.register_tool_function(get_video_deploy_results)

    return toolkit


def create_script_agent() -> ReActAgent:
    """创建脚本执行 Agent - 处理视综业务系统的Python脚本执行和API调用"""
    toolkit = create_video_system_toolkit()

    return ReActAgent(
        name="脚本执行Agent",
        sys_prompt="""你是一个视综业务系统执行专家。

你的职责是执行视综业务系统的任务。

--- 可用工具 ---
1. list_video_deploy_tasks(): 列出所有布控任务
2. create_video_deploy_task(): 创建新的布控任务
3. start_video_deploy_task(): 启动指定的布控任务
4. get_video_deploy_results(): 查看布控结果

--- 常见任务类型 ---
1. 查询布控任务列表
2. 创建新的布控任务（如：骑电动车未戴头盔、人群聚集检测）
3. 启动/停止布控任务
4. 查看布控报警结果

--- 执行流程 ---
1. 先调用 list_video_deploy_tasks 查看现有任务
2. 根据用户需求决定是查询、创建还是启动任务
3. 返回执行结果给用户

请根据用户需求，调用相应的工具函数来完成任务。""",
        model=create_model(),
        formatter=OpenAIChatFormatter(),
        memory=InMemoryMemory(),
        toolkit=toolkit,
    )


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
# 主程序 - 带状态的交互式会话
# ============================================================

class AgentSession:
    """智能体会话管理"""

    def __init__(self):
        self.current_agent: Optional[ReActAgent] = None
        self.current_agent_name: str = ""
        self.current_task_type: str = ""

    async def route_once(self, user_input: str) -> str:
        """首次路由，分配到对应的子智能体

        Args:
            user_input: 用户输入的任务描述

        Returns:
            路由结果描述
        """
        router = create_router_agent()
        msg_user = Msg(name="user", content=user_input, role="user")
        msg_response = await router(msg_user, structured_model=RoutingResult)

        routing_info = msg_response.metadata
        self.current_task_type = routing_info.get("task_type", "script")
        self.current_agent_name = routing_info.get("system", "")

        # 根据路由结果创建对应的子智能体
        if self.current_task_type == "script":
            self.current_agent = create_script_agent()
        elif self.current_task_type == "api":
            self.current_agent = create_api_agent()
        elif self.current_task_type == "gui":
            self.current_agent = create_gui_agent()
        else:
            return f"❌ 无法识别的任务类型: {self.current_task_type}"

        return f"已路由到 [{self.current_agent_name}]"

    async def chat(self, user_input: str) -> str:
        """与当前子智能体对话

        Args:
            user_input: 用户输入

        Returns:
            智能体响应
        """
        if self.current_agent is None:
            # 如果没有当前智能体，先进行路由
            await self.route_once(user_input)
            return "已自动路由，请继续输入..."

        msg = Msg(name="user", content=user_input, role="user")
        response = await self.current_agent(msg)
        return response.content

    def switch_agent(self, task_type: str) -> str:
        """切换到指定的智能体

        Args:
            task_type: 任务类型 (script/api/gui)

        Returns:
            切换结果
        """
        if task_type == "script":
            self.current_agent = create_script_agent()
            self.current_agent_name = "视综业务系统"
            self.current_task_type = "script"
        elif task_type == "api":
            self.current_agent = create_api_agent()
            self.current_agent_name = "自有业务系统"
            self.current_task_type = "api"
        elif task_type == "gui":
            self.current_agent = create_gui_agent()
            self.current_agent_name = "其他业务系统"
            self.current_task_type = "gui"
        else:
            return f"❌ 未知任务类型: {task_type}"

        return f"已切换到 [{self.current_agent_name}]"

    def reset(self):
        """重置会话"""
        self.current_agent = None
        self.current_agent_name = ""
        self.current_task_type = ""


async def main():
    """主程序入口"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         🚀 流程自动化智能体系统 v1.0                      ║
║                                                          ║
║   支持以下业务系统的任务自动路由与执行:                    ║
║   - 视综业务系统 (Python脚本/API调用)                      ║
║   - 自有业务系统 (API调用)                                 ║
║   - 其他业务系统 (视觉GUI操作)                            ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  命令说明:                                               ║
║    /route - 重新路由到新的任务                            ║
║    /switch script|api|gui - 切换到指定的业务系统         ║
║    /reset - 重置当前会话                                  ║
║    /quit - 退出程序                                       ║
╚══════════════════════════════════════════════════════════╝
    """)

    # 示例任务
    example_tasks = [
        "查询布控任务列表",
        "创建一个人群聚集检测任务",
        "查看布控报警结果",
    ]

    print("📝 示例任务:")
    for i, task in enumerate(example_tasks, 1):
        print(f"   {i}. {task}")
    print()

    # 创建会话管理器
    session = AgentSession()
    needs_routing = True  # 标记是否需要进行路由

    # 交互式输入
    while True:
        try:
            user_input = input(
                f"💬 [{session.current_agent_name or '未连接'}] 请输入 "
                f"({'/route 重新路由' if not needs_routing else ''}): "
            ).strip()

            if not user_input:
                continue

            # 处理特殊命令
            if user_input.lower() == '/quit':
                print("👋 再见!")
                break
            elif user_input.lower() == '/reset':
                session.reset()
                needs_routing = True
                print("🔄 会话已重置")
                continue
            elif user_input.lower().startswith('/switch '):
                task_type = user_input.split()[1]
                result = session.switch_agent(task_type)
                needs_routing = False
                print(result)
                continue
            elif user_input.lower() == '/route':
                session.reset()
                needs_routing = True
                print("🔄 请输入新任务进行路由...")
                continue

            # 正常对话流程
            if needs_routing:
                # 首次路由
                print("🔄 正在进行任务路由...")
                result = await session.route_once(user_input)
                print(f"✅ {result}")
                needs_routing = False
                print(f"💡 现在您已连接到 [{session.current_agent_name}]，可以直接输入任务")
            else:
                # 与当前智能体对话
                result = await session.chat(user_input)
                print(f"\n📤 执行结果:\n{result}\n")

        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"\n❌ 执行出错: {e}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
