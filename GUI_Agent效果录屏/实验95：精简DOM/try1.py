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

        if not (is_interactive or has_text or has_important_children):
            node.decompose()
            return None

        # 属性清理：只保留白名单属性
        attrs = node.attrs.copy()
        for attr in attrs:
            if attr not in ALLOWED_ATTRS:
                del node[attr]

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
