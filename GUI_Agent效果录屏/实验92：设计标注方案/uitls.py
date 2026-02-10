import re, os
from bs4 import BeautifulSoup, Comment, NavigableString

def save_simplified_html(original_html, simplified_html, output_folder="outputs", filename="simplified.html"):
    """
    保存精简后的 HTML 并输出统计信息
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, filename)

    # 1. 执行保存 (使用 utf-8 编码，防止 12306 等中文乱码)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(simplified_html)

    # 2. 计算压缩率 (Token 消耗通常与字符数成正比)
    orig_size = len(original_html)
    simp_size = len(simplified_html)
    reduction = (1 - simp_size / orig_size) * 100

    print("-" * 30)
    print(f"✅ 文件已保存至: {file_path}")
    print(f"📊 原始大小: {orig_size / 1024:.2f} KB")
    print(f"📊 简化后大小: {simp_size / 1024:.2f} KB")
    print(f"🚀 压缩率: {reduction:.1f}%")
    print("-" * 30)
    
def simplify_dom(html_content, max_text_length=100):
    """
    针对 12306 等复杂电商/票务网站设计的 DOM 简化工具
    """
    if not html_content:
        return ""

    # 使用 lxml 解析器（速度最快，容错最高）
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

    return simplified_html

# 使用示例
if __name__ == "__main__":
    # 假设你已经下载了 12306 的 HTML
    with open("12306.html", "r", encoding="utf-8") as f:
        html_data = f.read()
    
    simplified_result = simplify_dom(html_data)
    save_simplified_html(html_data, simplified_result, filename="for_agent.html")
