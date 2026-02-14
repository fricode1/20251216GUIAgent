"""
流程自动化主程序
管理整个流程自动化的执行流程
"""

from DrissionPage import Chromium
from script_generator import ScriptGenerator


class WorkflowAutomation:
    """流程自动化管理器"""
    
    def __init__(self, api_key: str = None):
        """
        初始化流程自动化管理器
        
        Args:
            api_key: 智谱AI API密钥，为None时使用默认密钥
        """
        self.script_generator = ScriptGenerator(api_key=api_key) if api_key else ScriptGenerator()
        self.browser = None
        self.tab = None
        self.current_script = self._get_initial_script()
        self.task_description = ""
    
    def _get_initial_script(self) -> str:
        """获取初始脚本模板"""
        return '''from DrissionPage import Chromium
from DrissionPage.common import Keys
import pyperclip
browser = Chromium()

tab = browser.latest_tab'''
    
    def start_browser(self):
        """启动浏览器"""
        self.browser = Chromium()
        self.tab = self.browser.latest_tab
        return self
    
    def set_task(self, task_description: str):
        """
        设置任务描述
        
        Args:
            task_description: 用户希望完成的流程自动化任务
        """
        self.task_description = task_description
        return self
    
    def get_current_dom(self) -> str:
        """
        获取当前页面的DOM内容
        
        Returns:
            当前页面的HTML内容
        """
        if self.tab is None:
            raise RuntimeError("浏览器未启动，请先调用start_browser()")
        return self.tab.html
    
    def generate_next_step(self) -> str:
        """
        生成下一步操作的脚本
        
        Returns:
            生成的Python脚本字符串
        """
        if not self.task_description:
            raise RuntimeError("任务描述未设置，请先调用set_task()")
        
        current_dom = self.get_current_dom()
        
        generated_script = self.script_generator.generate_next_step_script(
            task_description=self.task_description,
            current_script=self.current_script,
            current_dom=current_dom
        )
        
        return generated_script
    
    def execute_script(self, script: str):
        """
        执行生成的脚本
        
        Args:
            script: 要执行的Python脚本字符串
        """
        if self.browser is None:
            self.start_browser()
        
        # 创建执行环境，共享browser和tab对象
        exec_globals = {
            'Chromium': Chromium,
            'browser': self.browser,
            'tab': self.tab
        }
        
        exec(script, exec_globals)
        
        # 更新当前脚本
        self.current_script = script
    
    def run_step(self) -> str:
        """
        执行单步流程自动化
        
        Returns:
            执行的脚本内容
        """
        script = self.generate_next_step()
        self.execute_script(script)
        return script
    
    def close(self):
        """关闭浏览器"""
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
            self.tab = None
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        return False
