"""
Web界面后端服务
提供流程自动化的交互式界面
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from workflow_automation import WorkflowAutomation
from utils import truncate_dom
import threading
import queue
import traceback

app = Flask(__name__)
CORS(app)

# 全局状态
automation = None
action_queue = queue.Queue()
action_id_counter = 0


class ActionCard:
    """动作卡片数据结构"""
    def __init__(self, action_id, description, script, dom_snapshot, status="pending"):
        self.id = action_id
        self.description = description
        self.script = script
        self.dom_snapshot = dom_snapshot
        self.status = status  # pending, executing, completed, failed
        self.error = None

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "script": self.script,
            "dom_snapshot": self.dom_snapshot,
            "status": self.status,
            "error": self.error
        }


# 存储所有动作卡片
action_cards = []


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/init', methods=['POST'])
def init_automation():
    """初始化自动化流程"""
    global automation, action_cards, action_id_counter

    try:
        data = request.json
        url = data.get('url', 'https://www.12306.cn')
        task = data.get('task', '订一张从泰安到深圳的火车票')

        # 重置状态
        action_cards = []
        action_id_counter = 0

        # 初始化自动化
        automation = WorkflowAutomation()
        automation.start_browser()
        automation.tab.get(url)
        automation.set_task(task)

        return jsonify({
            "success": True,
            "message": "初始化成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/generate_next', methods=['POST'])
def generate_next_action():
    """生成下一个动作"""
    global automation, action_id_counter

    try:
        if automation is None:
            return jsonify({
                "success": False,
                "error": "自动化未初始化"
            }), 400

        # 生成下一步脚本
        script = automation.generate_next_step()

        # 获取当前DOM快照（使用truncate_dom处理）
        raw_dom = automation.get_current_dom()
        dom_snapshot = truncate_dom(raw_dom)

        # 生成动作描述
        description = extract_action_description(script)

        # 创建动作卡片
        action_id_counter += 1
        action_card = ActionCard(
            action_id=action_id_counter,
            description=description,
            script=script,
            dom_snapshot=dom_snapshot,
            status="pending"
        )

        action_cards.append(action_card)

        return jsonify({
            "success": True,
            "action": action_card.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/execute/<int:action_id>', methods=['POST'])
def execute_action(action_id):
    """执行指定的动作"""
    global automation

    try:
        # 查找动作卡片
        action_card = next((card for card in action_cards if card.id == action_id), None)

        if action_card is None:
            return jsonify({
                "success": False,
                "error": "动作不存在"
            }), 404

        if automation is None:
            return jsonify({
                "success": False,
                "error": "自动化未初始化"
            }), 400

        # 更新状态为执行中
        action_card.status = "executing"

        # 执行脚本
        automation.execute_script(action_card.script)

        # 更新状态为完成
        action_card.status = "completed"

        return jsonify({
            "success": True,
            "action": action_card.to_dict()
        })
    except Exception as e:
        # 更新状态为失败
        if action_card:
            action_card.status = "failed"
            action_card.error = str(e)

        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "action": action_card.to_dict() if action_card else None
        }), 500


@app.route('/api/actions', methods=['GET'])
def get_actions():
    """获取所有动作列表"""
    return jsonify({
        "success": True,
        "actions": [card.to_dict() for card in action_cards]
    })


@app.route('/api/action/<int:action_id>', methods=['GET'])
def get_action_detail(action_id):
    """获取动作详情"""
    action_card = next((card for card in action_cards if card.id == action_id), None)

    if action_card is None:
        return jsonify({
            "success": False,
            "error": "动作不存在"
        }), 404

    return jsonify({
        "success": True,
        "action": action_card.to_dict()
    })


@app.route('/api/close', methods=['POST'])
def close_automation():
    """关闭自动化"""
    global automation

    try:
        if automation:
            automation.close()
            automation = None

        return jsonify({
            "success": True,
            "message": "已关闭"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def extract_action_description(script: str) -> str:
    """
    从脚本中提取动作描述

    Args:
        script: Python脚本

    Returns:
        动作的自然语言描述
    """
    # 简单的启发式规则提取描述
    lines = script.split('\n')

    for line in lines:
        line = line.strip()

        # 查找点击操作
        if 'click' in line.lower():
            return f"点击元素"

        # 查找输入操作
        if 'type' in line.lower() or 'input' in line.lower():
            return f"输入文本"

        # 查找选择操作
        if 'select' in line.lower():
            return f"选择选项"

        # 查找等待操作
        if 'wait' in line.lower() or 'sleep' in line.lower():
            return f"等待页面加载"

    return "执行操作"


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
