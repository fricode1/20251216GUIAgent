"""
工具函数模块
提供流程自动化所需的辅助功能
"""

import re
from typing import Optional


def extract_xpath_selector(element_text: str) -> Optional[str]:
    """
    从文本中提取xpath选择器
    
    Args:
        element_text: 包含选择器的文本
        
    Returns:
        提取到的xpath选择器，如果没有则返回None
    """
    xpath_pattern = r'xpath://[^\s"\'\]]+'
    match = re.search(xpath_pattern, element_text)
    return match.group(0) if match else None


def format_xpath_selector(xpath: str) -> str:
    """
    格式化xpath选择器，确保以xpath:开头
    
    Args:
        xpath: xpath字符串
        
    Returns:
        格式化后的xpath选择器
    """
    if not xpath.startswith("xpath:"):
        return f"xpath:{xpath}"
    return xpath

import re, os
from bs4 import BeautifulSoup, Comment, NavigableString
def truncate_dom(html_content, max_text_length=1000000):
    soup = BeautifulSoup(html_content, 'lxml')

    # 1. 彻底移除绝对无用的标签
    REMOVAL_LIST = [
        'script', 'style', 'link', 'meta', 'noscript', 'svg', 'iframe', 'canvas', 
        'header', 'footer', 'head', 'img', 'video', 'audio', 'map', 'area'
    ]
    for tag in soup.find_all(REMOVAL_LIST):
        tag.decompose()

    # 2. 关键属性白名单（极简主义）
    # 增加 data-val, data-code 等 12306 常见的关键属性
    ALLOWED_ATTRS = {
        'id', 'name', 'placeholder', 'value', 'href', 'role', 
        'type', 'aria-label', 'data-terminal'
    }

    # 3. 递归清理逻辑
    def clean_node(node):
        if isinstance(node, NavigableString):
            # 清理纯空白字符
            content = node.strip()
            if not content:
                return None
            # 限制超长文本（12306 有时会有很长的隐藏条款）
            if len(content) > max_text_length:
                return NavigableString(content[:max_text_length] + "...")
            return node

        # 获取子节点
        children = list(node.children)
        for child in children:
            clean_node(child)

        # 判断是否为交互元素
        is_interactive = node.name in {'a', 'button', 'input', 'select', 'textarea'} or \
                         node.has_attr('onclick') or \
                         node.get('role') in ['button', 'checkbox', 'tab'] or \
                         'btn' in str(node.get('class', [])) # 12306 常用 class 标识按钮

        # 判断是否有文本内容
        has_text = any(isinstance(c, NavigableString) and c.strip() for c in node.children)
        # 判断是否有关键子节点
        has_important_children = any(c.name is not None for c in node.children)

        # 决策：是否保留该节点
        # 如果是交互元素，保留
        # 如果包含文本（车次、时间、余票），保留
        # 如果什么都没有，删除
        if not (is_interactive or has_text or has_important_children):
            node.decompose()
            return None

        # 属性清理：只保留白名单属性
        attrs = node.attrs.copy()
        for attr in attrs:
            if attr not in ALLOWED_ATTRS:
                del node[attr]

        # 12306 特有：将一些深层嵌套的 div 转换为更简单的结构（降维）
        # 如果 div 只有一个文本子节点，且没有属性，可以考虑去掉这一层
        if node.name == 'div' and len(node.contents) == 1 and isinstance(node.contents[0], NavigableString):
             # 保持结构简单，不强制转换但清理冗余
             pass

        return node

    # 执行清理
    body = soup.find('body')
    if not body:
        body = soup
    
    clean_node(body)

    # 4. 再次后处理：移除连续的空行和多余空白
    simplified_html = soup.decode(formatter="minimal")
    # 使用正则进一步压缩
    simplified_html = re.sub(r'\s*\n\s*', '\n', simplified_html) # 压缩换行
    simplified_html = re.sub(r' +', ' ', simplified_html)      # 压缩空格

    print('DOM精简完成')
    print(simplified_html)
    return simplified_html


def clean_script(script: str) -> str:
    """
    清理脚本内容，移除不必要的标记和注释
    
    Args:
        script: 原始脚本内容
        
    Returns:
        清理后的脚本内容
    """
    # 移除markdown代码块标记
    script = re.sub(r'```python\s*\n', '', script)
    script = re.sub(r'```\s*', '', script)
    
    # 移除行号标记（如 "123→"）
    script = re.sub(r'^\s*\d+→', '', script, flags=re.MULTILINE)
    
    return script.strip()


def validate_script(script: str) -> tuple[bool, str]:
    """
    验证脚本的基本语法正确性
    
    Args:
        script: 要验证的脚本
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        compile(script, '<string>', 'exec')
        return True, ""
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"验证错误: {e}"


def merge_scripts(base_script: str, new_script: str) -> str:
    """
    合并两个脚本，保留新脚本的操作部分
    
    Args:
        base_script: 基础脚本（包含导入和初始化）
        new_script: 新脚本（包含具体操作）
        
    Returns:
        合并后的脚本
    """
    # 如果新脚本已经包含完整导入，直接返回
    if 'from DrissionPage import Chromium' in new_script:
        return new_script
    
    # 否则合并脚本
    base_lines = base_script.strip().split('\n')
    new_lines = new_script.strip().split('\n')
    
    # 找到base_script中导入语句结束的位置
    import_end = 0
    for i, line in enumerate(base_lines):
        if line.strip() and not line.startswith('from ') and not line.startswith('import '):
            import_end = i
            break
    
    # 合并：base的导入 + 新脚本的所有内容
    merged = '\n'.join(base_lines[:import_end]) + '\n\n' + '\n'.join(new_lines)
    return merged


def save_script(script: str, filepath: str):
    """
    保存脚本到文件
    
    Args:
        script: 脚本内容
        filepath: 文件路径
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(script)


def load_script(filepath: str) -> str:
    """
    从文件加载脚本
    
    Args:
        filepath: 文件路径
        
    Returns:
        脚本内容
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
