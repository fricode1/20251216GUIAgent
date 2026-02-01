import os
import re

def sanitize_filename(name):
    """
    根据要求处理文件名：
    1. 将冒号 : 替换为 " -"（空格+连字符）
    2. 移除 Markdown 格式字符
    3. 替换其他非法字符为下划线
    """
    # 1. 移除常见的 Markdown 格式（如 **粗体**）
    name = re.sub(r'[*_`#]', '', name)
    name = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', name)
    
    # 2. 关键步骤：将冒号替换为 " -"
    # 兼容中文冒号 ： 和英文冒号 :
    name = name.replace(':', ' -').replace('：', ' -')
    
    # 3. 替换其他操作系统不允许的非法字符 (\ / * ? " < > |)
    name = re.sub(r'[\\/*?"<>|]', '_', name)
    
    # 4. 修整多余空格并返回
    return name.strip()

def split_markdown_by_h1(input_file):
    if not os.path.exists(input_file):
        print(f"错误: 找不到文件 {input_file}")
        return

    # 1. 以原文件名创建文件夹
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = base_name
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")

    # 2. 读取内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. 匹配一级标题进行拆分
    # 正则：匹配行首的 #，捕获其后的标题文字
    # ^#\s+ 确保只匹配一级标题（# 后跟空格），不匹配二级标题（##）
    pattern = r'^#\s+(.+)$'
    parts = re.split(pattern, content, flags=re.MULTILINE)

    # parts[0] 是第一个一级标题前的内容（序言）
    preface = parts[0].strip()
    sections = parts[1:]

    # 4. 保存序言（如有）
    if preface:
        with open(os.path.join(output_dir, "00_前言.txt"), 'w', encoding='utf-8') as f:
            f.write(preface)

    # 5. 遍历保存每个一级标题段落
    for i in range(0, len(sections), 2):
        raw_title = sections[i].strip()
        body = sections[i+1].strip()
        
        # 处理文件名
        safe_title = sanitize_filename(raw_title)
        
        # 防止标题处理后变成空字符串
        if not safe_title:
            safe_title = f"section_{i//2 + 1}"
            
        filename = f"{safe_title}.txt"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(body)
            
        print(f"已生成: {file_path}")

if __name__ == "__main__":
    # 使用示例：将 test.md 替换为你实际的文件名
    target_md = r'C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验87：双语播客\data\人类理解论第二卷\locke1690book2_one_sentence_per_line.md'
    split_markdown_by_h1(target_md)