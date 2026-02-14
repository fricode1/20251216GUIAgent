"""
最终执行脚本
整合所有模块，提供完整的流程自动化功能
"""

from DrissionPage import Chromium
from script_generator import ScriptGenerator
from utils import save_script, validate_script


def run_workflow_automation(
    task_description: str,
    initial_url: str = None,
    max_steps: int = 10,
    api_key: str = None
):
    """
    运行完整的流程自动化任务
    
    Args:
        task_description: 任务描述，例如"订一张从泰安到重庆东的火车票"
        initial_url: 初始URL，如果为None则需要在调用前手动打开浏览器
        max_steps: 最大执行步数，防止无限循环
        api_key: 智谱AI API密钥
        
    Returns:
        执行的所有脚本列表
    """
    generator = ScriptGenerator(api_key=api_key) if api_key else ScriptGenerator()
    browser = Chromium()
    tab = browser.latest_tab
    
    executed_scripts = []
    
    try:
        # 访问初始URL
        if initial_url:
            tab.get(initial_url)
        
        # 初始脚本
        current_script = '''from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Keys
import pyperclip
co = ChromiumOptions().auto_port()
browser = Chromium(co)
tab = browser.latest_tab'''
        
        print(f"开始执行任务: {task_description}")
        print("=" * 60)
        
        for step in range(1, max_steps + 1):
            print(f"\n--- 第 {step} 步 ---")
            
            # 获取当前DOM
            current_dom = tab.html
            
            # 生成下一步脚本
            generated_script = generator.generate_next_step_script(
                task_description=task_description,
                current_script=current_script,
                current_dom=current_dom
            )
            
            print("生成的脚本:")
            print(generated_script)
            print()
            
            # 验证脚本
            is_valid, error = validate_script(generated_script)
            if not is_valid:
                print(f"脚本验证失败: {error}")
                break
            
            # 执行脚本
            try:
                exec_globals = {
                    'Chromium': Chromium,
                    'browser': browser,
                    'tab': tab
                }
                exec(generated_script, exec_globals)
                executed_scripts.append(generated_script)
                current_script = generated_script
                
                # 保存每一步的脚本
                save_script(generated_script, f"step_{step}.py")
                print(f"脚本已保存到 step_{step}.py")
                
            except Exception as e:
                print(f"执行脚本时出错: {e}")
                break
            
            # 询问是否继续（可以改为自动判断）
            user_input = input("是否继续下一步? (y/n): ").strip().lower()
            if user_input != 'y':
                print("用户终止执行")
                break
        
        print("\n" + "=" * 60)
        print(f"任务执行完成，共执行 {len(executed_scripts)} 步")
        
    finally:
        browser.quit()
    
    return executed_scripts


def generate_single_step(
    task_description: str,
    current_script: str,
    current_dom: str,
    api_key: str = None
) -> str:
    """
    生成单步脚本（无需浏览器环境）
    
    Args:
        task_description: 任务描述
        current_script: 当前已生成的脚本
        current_dom: 当前页面DOM
        api_key: API密钥
        
    Returns:
        生成的脚本
    """
    generator = ScriptGenerator(api_key=api_key) if api_key else ScriptGenerator()
    
    generated_script = generator.generate_next_step_script(
        task_description=task_description,
        current_script=current_script,
        current_dom=current_dom
    )
    
    return generated_script


if __name__ == "__main__":
    import sys
    
    # 命令行参数支持
    if len(sys.argv) > 1:
        task = sys.argv[1]
        url = sys.argv[2] if len(sys.argv) > 2 else None
        run_workflow_automation(task, url)
    else:
        # 示例任务
        example_task = "订一张从泰安到重庆东的火车票"
        example_url = "https://www.12306.cn"
        
        print("用法: python final_script.py <任务描述> [初始URL]")
        print(f"\n示例任务: {example_task}")
        print(f"示例URL: {example_url}")
        print("\n直接运行将使用示例任务...")
        
        # 取消下面一行的注释以运行示例
        # run_workflow_automation(example_task, example_url)
