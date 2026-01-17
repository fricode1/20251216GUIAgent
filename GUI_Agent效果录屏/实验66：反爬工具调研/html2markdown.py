from markdownify import markdownify as md

# 1. 读取本地 HTML 文件
file_path = 'collection_page.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 2. 转换为 Markdown
# heading_style="ATX" 会将标题转为 # 格式，而不是底线格式
markdown_text = md(html_content, heading_style="ATX")

# 3. 保存结果
with open('collection_page.md', 'w', encoding='utf-8') as f:
    f.write(markdown_text)

print("转换完成！")