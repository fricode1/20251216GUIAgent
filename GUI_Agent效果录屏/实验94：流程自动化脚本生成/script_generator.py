"""
脚本生成器模块
根据用户任务、已有脚本和当前网页内容生成下一步操作的Python脚本
"""

from zai import ZhipuAiClient
from utils import truncate_dom

class ScriptGenerator:
    """流程自动化脚本生成器"""
    
    def __init__(self, api_key: str = "5aab6fda6039467ebe3c011e5935b856.FrUFg7WiNub5cLYp"):
        """
        初始化脚本生成器
        
        Args:
            api_key: 智谱AI API密钥
        """
        self.client = ZhipuAiClient(api_key=api_key)
        self.model = "glm-5"
    
    def generate_next_step_script(
        self,
        task_description: str,
        current_script: str,
        current_dom: str
    ) -> str:
        """
        生成下一步操作的Python脚本
        
        Args:
            task_description: 用户希望完成的流程自动化任务描述
            current_script: 已经生成的流程自动化完整Python脚本
            current_dom: 当前网页的DOM内容
            
        Returns:
            生成的完整Python脚本，用于执行下一步操作
        """
        prompt = self._build_prompt(task_description, current_script, current_dom)
        
        print('开始调用大模型')
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
        )
        
        generated_script = response.choices[0].message.content
        return self._extract_code(generated_script)
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个专业的流程自动化脚本生成专家。
你的任务是根据用户任务、已有脚本和当前网页DOM，生成下一步操作的Python脚本。

重要规则：
1. 只生成下一步操作，不要生成多步操作
2. 生成的脚本必须是完整的、可执行的Python代码
3. 使用DrissionPage库进行浏览器自动化
4. 元素选择器必须以 "xpath:" 开头
5. 点击操作使用 tab.actions.click(ele_selector)
6. 列表选择使用 list_ele.select.by_text('xxx')
7. 确保脚本包含必要的导入语句
8. 脚本应该基于current_script继续执行，而不是从头开始
- 如果要填写文本框，需要先清除原有内容，再输入新内容。
- 如果要填写文本框，要先将待填写的内容放入剪贴板（记得 import pyperclip），然后使用 `tab.actions.type((Keys.CTRL_A, Keys.CTRL_V))` 方法。
- 严禁使用索引 ID：禁止使用类似 citem_0, list-item-1 这种包含数字索引的 ID，因为列表顺序是随机的。
- 变量即核心：操作的目标（如“泰安”）是一个变量。选择器必须包含该文本内容。

输出格式要求：
- 只输出Python代码，不要输出任何解释文字
- 代码必须完整，包含所有必要的导入
- 代码必须使用已存在的browser和tab对象（如果current_script中已创建）"""

    def _build_prompt(
        self,
        task_description: str,
        current_script: str,
        current_dom: str
    ) -> str:
        current_dom = truncate_dom(current_dom)
        """构建提示词"""
        return f"""请根据以下信息生成下一步操作的Python脚本：

## 用户任务
{task_description}

## 已生成的脚本
```python
{current_script}
```

## 当前网页DOM
```html
{current_dom}
```

请分析当前状态，生成执行下一步操作的完整Python脚本。
注意：
1. 只生成下一步操作
2. 脚本必须是完整的、可执行的
3. 如果current_script中已创建browser和tab对象，请继续使用它们
4. 元素选择器使用xpath格式，以"xpath:"开头
5. 点击操作使用 tab.actions.click(ele_selector)
6. 列表选择使用 list_ele.select.by_text('xxx')
- 单步操作的粒度要尽量小。比如，文本的填写与下拉框的选择，是2步操作，不是单步操作。

请只输出Python代码，不要包含任何解释。"""

    def _extract_code(self, text: str) -> str:
        """从文本中提取代码块"""
        import re
        
        # 尝试提取markdown代码块
        code_pattern = r'```python\s*\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        if matches:
            return matches[-1].strip()
        
        # 如果没有markdown代码块，尝试提取普通代码块
        code_pattern = r'```\s*\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        if matches:
            return matches[-1].strip()
        
        # 如果都没有，返回原文本
        return text.strip()
