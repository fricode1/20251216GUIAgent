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
        # 启动浏览器（不访问网站）
        automation.start_browser()

        # 设置任务（包含访问网站的指令）
        automation.set_task("访问 https://www.12306.cn，然后订一张从泰安到深圳的火车票")

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
