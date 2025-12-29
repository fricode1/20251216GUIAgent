import sys
import os
import asyncio
import threading
import time
from datetime import datetime

# 核心界面库
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont, QTextCursor

# 你的业务库
from browser_use.agent.service import Agent
from browser_use import ChatOpenAI, Browser

# --- 1. 定义工作线程，防止界面卡死 ---
class AgentWorker(QThread):
    # 定义信号，用于把信息传回主界面显示
    info_signal = Signal(str, str)  # 角色, 内容
    finished_signal = Signal()

    def __init__(self, task_prompt):
        super().__init__()
        self.task_prompt = task_prompt

    def run(self):
        # 在子线程启动新的异步事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.execute_task())
        loop.close()

    async def execute_task(self):
        try:
            # 你的配置逻辑
            api_key = 'sk-efe1c9004f7e4de0a8ade26120301c6d'
            base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
            model = 'qwen-vl-max'
            llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

            executable_path = '/usr/bin/google-chrome'
            user_data_dir = os.path.expanduser('~/.config/google-chrome')

            browser = Browser(
                executable_path=executable_path,
                user_data_dir=user_data_dir,
                profile_directory='Default',
            )

            agent = Agent(task=self.task_prompt, llm=llm, use_vision=False, browser=browser)
            
            self.info_signal.emit("Agent", "正在启动浏览器执行任务...")
            start_time = time.time()
            
            # 运行 Agent
            await agent.run()
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.info_signal.emit("Agent", f"任务已完成！耗时: {duration}s")
        
        except Exception as e:
            self.info_signal.emit("Error", str(e))
        finally:
            self.finished_signal.emit()

# --- 2. 主界面窗口 ---
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Browser Agent 控制台")
        self.resize(700, 800)

        # 设置默认字体
        font = QFont("Sans Serif", 11)
        self.setFont(font)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 聊天显示区
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.chat_display)

        # 输入栏布局
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入任务指令...")
        self.input_field.setFixedHeight(40)
        self.input_field.returnPressed.connect(self.handle_send)
        
        self.send_btn = QPushButton("启动 Agent")
        self.send_btn.setFixedHeight(40)
        self.send_btn.setFixedWidth(100)
        self.send_btn.clicked.connect(self.handle_send)
        self.send_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        self.append_text("System", "准备就绪。请输入任务并点击启动。")

    def append_text(self, role, content):
        time_str = datetime.now().strftime("%H:%M:%S")
        color = "#000000"
        if role == "User": color = "#0056b3"
        elif role == "Agent": color = "#28a745"
        elif role == "Error": color = "#dc3545"

        html_text = f"""
        <div style='margin-bottom: 10px;'>
            <b style='color: {color};'>[{time_str}] {role}:</b><br/>
            <span style='color: #333;'>{content.replace("\n", "<br/>")}</span>
        </div>
        """
        self.chat_display.append(html_text)
        self.chat_display.moveCursor(QTextCursor.End)

    def handle_send(self):
        task = self.input_field.text().strip()
        if not task: return

        self.append_text("User", task)
        self.input_field.clear()
        self.send_btn.setEnabled(False)

        # 创建并启动后台线程
        self.worker = AgentWorker(task)
        self.worker.info_signal.connect(self.append_text)
        self.worker.finished_signal.connect(lambda: self.send_btn.setEnabled(True))
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 解决高分屏显示问题的设置
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())