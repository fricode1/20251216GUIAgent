"""
使用示例
演示如何使用流程自动化脚本生成器
"""

from workflow_automation import WorkflowAutomation
from script_generator import ScriptGenerator
from utils import save_script, load_script, validate_script


def example_basic_usage():
    """
    基础使用示例
    演示完整的流程自动化步骤
    """
    # 定义任务
    task = "订一张从泰安到重庆东的火车票"
    
    # 使用上下文管理器创建自动化实例
    with WorkflowAutomation() as automation:
        # 启动浏览器
        automation.start_browser()
        
        # 设置任务
        automation.set_task(task)
        
        # 获取当前页面DOM（假设已经打开了12306网站）
        # current_dom = automation.get_current_dom()
        
        # 生成并执行下一步脚本
        # script = automation.run_step()
        # print("生成的脚本:")
        # print(script)


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
        automation.set_task("订一张从泰安到重庆东的火车票")

        while True:
            print("=== 生成脚本 ===")
            script1 = automation.generate_next_step()
            print(script1)
            automation.execute_script(script1)
            input("按回车继续...")
    finally:
        automation.close()


def example_direct_generator():
    """
    直接使用生成器示例
    演示如何直接使用ScriptGenerator生成脚本
    """
    generator = ScriptGenerator()
    
    task_description = "订一张从泰安到重庆东的火车票"
    
    current_script = '''from DrissionPage import Chromium

browser = Chromium()

tab = browser.latest_tab'''
    
    # 模拟当前页面的DOM（实际使用时从浏览器获取）
    current_dom = '''
    <html>
    <body>
        <div id="search">
            <input id="fromStation" placeholder="出发地" />
            <input id="toStation" placeholder="目的地" />
            <input id="train_date" placeholder="出发日期" />
            <button id="search_button">查询</button>
        </div>
    </body>
    </html>
    '''
    
    # 生成下一步脚本
    generated_script = generator.generate_next_step_script(
        task_description=task_description,
        current_script=current_script,
        current_dom=current_dom
    )
    
    print("生成的脚本:")
    print(generated_script)
    
    # 验证脚本
    is_valid, error = validate_script(generated_script)
    if is_valid:
        print("\n脚本验证通过")
        # 保存脚本
        save_script(generated_script, "generated_step.py")
        print("脚本已保存到 generated_step.py")
    else:
        print(f"\n脚本验证失败: {error}")


def example_with_custom_api_key():
    """
    使用自定义API密钥示例
    """
    # 使用自定义API密钥
    custom_api_key = "your-api-key-here"
    automation = WorkflowAutomation(api_key=custom_api_key)
    
    # 其余操作与基础示例相同
    automation.start_browser()
    automation.set_task("查询北京到上海的航班")
    
    # ... 后续操作
    
    automation.close()


if __name__ == "__main__":
    print("=== 流程自动化脚本生成器使用示例 ===\n")
    
    print("1. 基础使用示例 (需要浏览器环境)")
    print("   运行: example_basic_usage()")
    
    print("\n2. 分步执行示例 (需要浏览器环境)")
    print("   运行: example_step_by_step()")
    
    print("\n3. 直接使用生成器示例 (无需浏览器)")
    print("   运行: example_direct_generator()")
    
    print("\n4. 使用自定义API密钥示例")
    print("   运行: example_with_custom_api_key()")
    
    # 默认运行直接生成器示例（无需浏览器）
    print("\n" + "="*50)
    print("正在运行: example_direct_generator()")
    print("="*50 + "\n")
    example_step_by_step()
