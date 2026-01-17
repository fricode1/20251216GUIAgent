#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取页面完整内容并转换为Markdown"""

import re
import sys
import json
import html
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_full_content(html_file):
    """提取完整内容"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    items = []

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

            # 提取赞同数(从文本中)
            vote_elem = card.select_one('.VoteButton--up')
            vote_count = ''
            if vote_elem:
                vote_text = vote_elem.get_text(strip=True)
                vote_count = vote_text

            item = {
                'index': i,
                'title': title,
                'question_link': question_link,
                'author_name': author_name,
                'author_link': author_link,
                'avatar': avatar_url,
                'content': content_text,
                'item_id': item_id,
                'vote_count': vote_count
            }

            items.append(item)

        except Exception as e:
            print(f"处理第{i}个卡片时出错: {e}")
            continue

    return items

def save_to_markdown(items, output_file):
    """保存为Markdown格式"""

    md_content = """# 赞同超过10K的回答 - 知乎收藏夹

> 来源：知乎收藏夹
> 收录时间：2025-01-17

---

"""

    for item in items:
        md_content += f"""## {item['index']}. {item['title']}

**问题链接**: [{item['question_link']}]({item['question_link']})

**作者**: [{item['author_name']}]({item['author_link']})

**回答ID**: {item['item_id']}

---

### 回答内容

{item['content'] if item['content'] else '*（内容需要展开查看）*'}

---

**相关链接**:
- [查看完整回答]({item['question_link']})
- [作者主页]({item['author_link']})

---

"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✓ Markdown文件已保存: {output_file}")

def main():
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'
    output_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\收藏夹内容.md'

    print("=" * 80)
    print("提取知乎收藏夹内容并转换为Markdown")
    print("=" * 80)
    print()

    items = extract_full_content(html_file)

    print(f"成功提取 {len(items)} 个回答\n")

    save_to_markdown(items, output_file)

    print("\n" + "=" * 80)
    print("转换完成!")
    print("=" * 80)

if __name__ == '__main__':
    main()
