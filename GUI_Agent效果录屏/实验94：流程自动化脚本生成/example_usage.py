from workflow_automation import WorkflowAutomation
from script_generator import ScriptGenerator
from utils import save_script, load_script, validate_script


def example_step_by_step():
    """
    分步执行示例
    演示如何逐步生成和执行脚本
    """
    automation = WorkflowAutomation()
    
    try:
        # 启动浏览器并访问目标网站
        automation.start_browser()
        automation.tab.get("https://www.12306.cn")
        
        # 设置任务
        automation.set_task("订一张从泰安到深圳的火车票")

        while True:
            print("=== 生成脚本 ===")
            script1 = automation.generate_next_step()
            print(script1)
            automation.execute_script(script1)
            input("按回车继续...")
    finally:
        automation.close()

if __name__ == "__main__":
    example_step_by_step()
