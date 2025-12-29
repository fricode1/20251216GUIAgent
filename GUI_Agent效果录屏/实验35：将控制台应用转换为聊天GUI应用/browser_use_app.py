import sys
import os
import asyncio
import threading
import time
import logging
from datetime import datetime

# PySide6 核心组件
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QSplitter, QLabel)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QObject
from PySide6.QtGui import QFont, QTextCursor

# 业务组件
from browser_use.agent.service import Agent
from browser_use import ChatOpenAI, Browser

# --- 1. 日志与输出重定向系统 ---

class LogSignaler(QObject):
    """跨线程发送文本信号的桥梁"""
    new_text = Signal(str)

class QtLogHandler(logging.Handler):
    """拦截 logging 模块产生的日志并发送信号"""
    def __init__(self, signaler):
        super().__init__()
        self.signaler = signaler

    def emit(self, record):
        msg = self.format(record)
        self.signaler.new_text.emit(msg + "\n")

class StdoutRedirector:
    """拦截 sys.stdout.write (即 print) 并发送信号"""
    def __init__(self, signaler):
        self.signaler = signaler

    def write(self, text):
        if text:
            self.signaler.new_text.emit(str(text))

    def flush(self):
        pass

# --- 2. 后台执行线程 ---

class AgentWorker(QThread):
    """在独立线程中运行异步 Agent 逻辑，防止 GUI 卡死"""
    finished_signal = Signal()

    def __init__(self, task_prompt):
        super().__init__()
        self.task_prompt = task_prompt

    def run(self):
        # 为当前线程创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.execute_task())
        finally:
            loop.close()
            self.finished_signal.emit()

    async def execute_task(self):
        try:
            # 配置你的 LLM 和 浏览器（从你的代码中提取）
            api_key = 'sk-efe1c9004f7e4de0a8ade26120301c6d'
            base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
            model = 'qwen-vl-max'
            
            llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

            browser = Browser(
                executable_path='/usr/bin/google-chrome',
                user_data_dir=os.path.expanduser('~/.config/google-chrome'),
                profile_directory='Default',
            )

            agent = Agent(
                task=self.task_prompt,
                llm=llm,
                use_vision=False,
                browser=browser,
            )

            print(f"\n>>> [系统启动] 正在执行任务: {self.task_prompt}")
            start_time = time.time()
            
            # 执行核心逻辑
            await agent.run()
            
            duration = round(time.time() - start_time, 2)
            print(f"\n>>> [系统完成] 耗时 {duration} 秒")

        except Exception as e:
            logging.error(f"Agent运行时异常: {str(e)}")

# --- 3. 主窗口界面 ---

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Agent 自动化操作台")
        self.resize(1000, 800)

        # 初始化重定向信号源
        self.signaler = LogSignaler()
        self.signaler.new_text.connect(self.append_raw_log)

        # 布局初始化
        self.setup_ui()
        
        # 核心：启动日志拦截
        self.setup_logging_interception()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 使用 QSplitter 实现可调节的上下分栏
        self.splitter = QSplitter(Qt.Vertical)

        # 上部分：简化的聊天/状态展示区
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("这里显示关键任务状态...")
        self.chat_display.setStyleSheet("background-color: #ffffff; border: 1px solid #ddd; padding: 10px;")
        
        # 下部分：原始日志控制台区
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(0, 5, 0, 0)
        log_layout.addWidget(QLabel("系统实时运行日志 (Terminal Output):"))
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        # 使用等宽字体，模拟终端感觉
        self.log_display.setFont(QFont("Monospace", 9))
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e; 
                color: #d4d4d4; 
                border: none;
            }
        """)
        log_layout.addWidget(self.log_display)

        self.splitter.addWidget(self.chat_display)
        self.splitter.addWidget(log_container)
        self.splitter.setStretchFactor(0, 1) # 比例
        self.splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(self.splitter)

        # 输入区域
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("请输入指令（若无法输入中文，请粘贴）...")
        self.input_field.setFixedHeight(45)
        self.input_field.returnPressed.connect(self.handle_send)
        
        self.send_btn = QPushButton("启动任务")
        self.send_btn.setFixedHeight(45)
        self.send_btn.setFixedWidth(120)
        self.send_btn.setStyleSheet("background-color: #0078d4; color: white; font-weight: bold;")
        self.send_btn.clicked.connect(self.handle_send)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        main_layout.addLayout(input_layout)

    def setup_logging_interception(self):
        """核心方法：拦截全局日志"""
        # 1. 重定向 sys.stdout/stderr (针对 print)
        sys.stdout = StdoutRedirector(self.signaler)
        sys.stderr = StdoutRedirector(self.signaler)

        # 2. 接管 logging 模块
        handler = QtLogHandler(self.signaler)
        formatter = logging.Formatter('%(levelname)s [%(name)s] %(message)s')
        handler.setFormatter(formatter)

        # 获取根记录器
        root_logger = logging.getLogger()
        # 清除已有的处理器（防止重复输出到终端）
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

        # 3. 针对性强制拦截 browser-use 和 playwright 相关库
        # 即使它们内部自己创建了记录器，这几行也能抓到
        for logger_name in ['browser_use', 'agent', 'langchain', 'playwright']:
            l = logging.getLogger(logger_name)
            l.propagate = True # 确保它们向上传递到根记录器
            l.setLevel(logging.INFO)

    @Slot(str)
    def append_raw_log(self, text):
        """将拦截到的文本追到黑色控制台区"""
        self.log_display.moveCursor(QTextCursor.End)
        self.log_display.insertPlainText(text)
        # 保持滚动条在最下方
        self.log_display.moveCursor(QTextCursor.End)

    def handle_send(self):
        task = self.input_field.text().strip()
        if not task:
            return

        # UI 更新
        self.chat_display.append(f"<b style='color:#0078d4;'>[User]:</b> {task}<br>")
        self.input_field.clear()
        self.send_btn.setEnabled(False)

        # 启动后台线程
        self.worker = AgentWorker(task)
        self.worker.finished_signal.connect(lambda: self.send_btn.setEnabled(True))
        self.worker.start()

    def closeEvent(self, event):
        """退出时恢复标准输出，防止崩溃"""
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        super().closeEvent(event)

if __name__ == "__main__":
    # 处理高分屏缩放
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    
    # 设置应用全局字体（解决 Linux 下部分字体渲染难看问题）
    default_font = QFont("Sans Serif", 10)
    app.setFont(default_font)

    window = ChatWindow()
    window.show()
    
    sys.exit(app.exec())