import re, os
from bs4 import BeautifulSoup, Comment, NavigableString

def truncate_dom(html_content, max_text_length=1000000):
    soup = BeautifulSoup(html_content, 'lxml')

    # 1. 移除注释
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # 2. 彻底移除无用标签
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
            content = node.strip()
            if not content:
                return None
            if len(content) > max_text_length:
                return NavigableString(content[:max_text_length] + "...")
            return node

        # 先递归清理子节点
        children = list(node.children)
        for child in children:
            clean_node(child)

        # 判断是否为交互元素
        is_interactive = node.name in {'a', 'button', 'input', 'select', 'textarea'} or \
                         node.has_attr('onclick') or \
                         node.get('role') in ['button', 'checkbox', 'tab', 'menuitem', 'menuitemradio'] or \
                         'btn' in str(node.get('class', []))

        # 获取所有文本内容（递归）
        text_content = node.get_text(strip=True)
        has_text = bool(text_content)

        # 判断是否有重要子节点
        has_important_children = any(c.name in {'a', 'button', 'input', 'select', 'textarea', 'ul', 'li'}
                                     for c in node.children if hasattr(c, 'name'))

        # 特殊处理：空链接直接删除
        if node.name == 'a' and not has_text and not node.find_all(['input', 'button']):
            node.decompose()
            return None

        # 空容器删除（除非是表单元素）
        if not (is_interactive or has_text or has_important_children):
            node.decompose()
            return None

        # 属性清理
        attrs = node.attrs.copy()
        for attr in attrs:
            if attr not in ALLOWED_ATTRS:
                del node[attr]

        # 扁平化：如果div只有一个子元素且自己没有重要属性，考虑提升子元素
        if node.name == 'div' and len(list(node.children)) == 1:
            only_child = list(node.children)[0]
            # 如果子元素也是标签且父div没有重要属性
            if hasattr(only_child, 'name') and not any(node.get(attr) for attr in ALLOWED_ATTRS):
                node.replace_with(only_child)
                return only_child

        return node

    # 执行清理
    body = soup.find('body')
    if not body:
        body = soup

    clean_node(body)

    # 4. 后处理：压缩空白
    simplified_html = soup.decode(formatter="minimal")
    simplified_html = re.sub(r'\s*\n\s*', '\n', simplified_html)
    simplified_html = re.sub(r' +', ' ', simplified_html)
    # 移除空行
    simplified_html = re.sub(r'\n+', '\n', simplified_html)

    print('DOM精简完成')
    print(f'原始长度: {len(html_content)}, 精简后: {len(simplified_html)}, 压缩率: {(1-len(simplified_html)/len(html_content))*100:.1f}%')
    return simplified_html


if __name__ == '__main__':
    # 测试代码
    input_file = 'result1.html'  # 或者你的原始HTML文件
    output_file = 'result2.html'

    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            html = f.read()

        result = truncate_dom(html)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)

        print(f'\n结果已保存到: {output_file}')
    else:
        print(f'文件不存在: {input_file}')
