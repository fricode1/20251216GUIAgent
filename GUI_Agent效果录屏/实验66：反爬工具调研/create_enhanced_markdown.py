#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建增强版Markdown"""

import re
import sys
import json
import html
from bs4 import BeautifulSoup
from collections import Counter

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_enhanced_content(html_file):
    """提取增强内容"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    items = []
    authors = []
    topics = []

    # 查找所有回答卡片
    cards = soup.find_all(attrs={'data-zop': True})

    for i, card in enumerate(cards, 1):
        try:
            # 解析data-zop
            zop_str = card.get('data-zop', '{}')
            zop_data = json.loads(html.unescape(zop_str))

            # 提取问题标题
            title_elem = card.select_one('.ContentItem-title a')
            title = title_elem.get_text(strip=True) if title_elem else zop_data.get('title', '')

            # 提取问题链接
            question_link = ''
            if title_elem and title_elem.get('href'):
                href = title_elem['href']
                if href.startswith('//'):
                    question_link = 'https:' + href
                elif href.startswith('/'):
                    question_link = 'https://www.zhihu.com' + href
                else:
                    question_link = href

            # 提取作者信息
            author_name_elem = card.select_one('.AuthorInfo-name')
            author_name = author_name_elem.get_text(strip=True) if author_name_elem else zop_data.get('authorName', '')

            # 收集作者
            if author_name:
                authors.append(author_name)

            author_link_elem = card.select_one('.AuthorInfo-name')
            author_link = ''
            if author_link_elem and author_link_elem.get('href'):
                href = author_link_elem['href']
                if href.startswith('//'):
                    author_link = 'https:' + href
                elif href.startswith('/'):
                    author_link = 'https://www.zhihu.com' + href

            # 提取作者头像
            avatar_elem = card.select_one('.AuthorInfo-avatarWrapper img')
            avatar_url = avatar_elem.get('src', '') if avatar_elem else ''

            # 提取正文内容
            content_div = card.select_one('.RichContent-inner')
            content_text = ''
            if content_div:
                # 提取段落
                paragraphs = content_div.find_all('p')
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

            # 提取元数据(itemId)
            item_id = zop_data.get('itemId', '')

            # 提取摘要(如果有)
            excerpt_elem = card.select_one('.RichContent-inner')
            excerpt = ''
            if excerpt_elem:
                text = excerpt_elem.get_text(strip=True)
                excerpt = text[:150] + '...' if len(text) > 150 else text

            item = {
                'index': i,
                'title': title,
                'question_link': question_link,
                'author_name': author_name,
                'author_link': author_link,
                'avatar': avatar_url,
                'content': content_text,
                'excerpt': excerpt,
                'item_id': item_id,
            }

            items.append(item)

        except Exception as e:
            print(f"处理第{i}个卡片时出错: {e}")
            continue

    return items, authors

def create_enhanced_markdown(items, authors, output_file):
    """创建增强版Markdown"""

    # 统计信息
    total_items = len(items)
    unique_authors = len(set(authors))

    # 创建目录
    toc = "\n".join([f"{i}. [{item['title']}](#{item['index']}-{item['title'][:30].replace(' ', '-')})" for i, item in enumerate(items, 1)])

    # 生成Markdown
    md_content = f"""# 赞同超过10K的回答 - 知乎收藏夹

<div align="center">

**收录数量**: {total_items} 个高质量回答
**独特作者**: {unique_authors} 位
**收录时间**: 2025-01-17

</div>

---

## 📋 目录

{toc}

---

## 📊 收藏夹统计

- 📝 **总回答数**: {total_items}
- 👤 **涉及作者**: {unique_authors}
- 💎 **质量标准**: 赞同数超过10K
- 📂 **收藏夹**: "赞同超过10K的回答"

---

## 📖 精选内容列表

"""

    for item in items:
        md_content += f"""
### {item['index']}. {item['title']}

<div align="center">

**作者**: [{item['author_name']}]({item['author_link']})
**回答ID**: `{item['item_id']}`
**链接**: [查看原回答]({item['question_link']})

</div>

---

**内容摘要**:

> {item['excerpt'] if item['excerpt'] else '*（点击上方链接查看完整回答）*'}

---

**快速导航**:
- 🔗 [完整回答]({item['question_link']})
- 👤 [作者主页]({item['author_link']})
- 💬 [查看评论]({item['question_link']})

---

"""

    md_content += """
## 🔍 使用说明

1. **查看内容**: 点击每个回答下方的"查看原回答"链接即可跳转到知乎页面
2. **作者信息**: 点击作者名称可以访问作者主页
3. **内容质量**: 本收藏夹所有回答赞同数均超过10K
4. **持续更新**: 收藏夹会不定期更新

## 📌 数据来源

- **来源**: 知乎收藏夹
- **收藏夹名称**: "赞同超过10K的回答"
- **提取时间**: 2025-01-17
- **工具**: HTML结构分析 + BeautifulSoup

## ⚠️ 免责声明

本Markdown文档仅供学习研究使用,所有内容版权归原作者所有。
如需查看完整内容,请访问知乎原页面。

---

<div align="center">

**Made with ❤️ by 知乎内容分析工具**

</div>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✓ 增强版Markdown文件已保存: {output_file}")

def main():
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'
    output_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\收藏夹内容_增强版.md'

    print("=" * 80)
    print("创建增强版Markdown文档")
    print("=" * 80)
    print()

    items, authors = extract_enhanced_content(html_file)

    print(f"成功提取 {len(items)} 个回答")
    print(f"涉及 {len(set(authors))} 位作者\n")

    create_enhanced_markdown(items, authors, output_file)

    print("\n" + "=" * 80)
    print("转换完成!")
    print("=" * 80)

if __name__ == '__main__':
    main()
