#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取页面中的实际数据样本"""

import re
import sys
import json
import html

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_samples(html_file):
    """提取关键数据样本"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 100)
    print("知乎页面 - 数据样本提取")
    print("=" * 100)

    # 1. 提取data-zop数据
    print("\n【1. data-zop 数据样本】")
    zop_pattern = r'data-zop=["\']({[^"\']+})["\']'
    zop_matches = re.findall(zop_pattern, content)

    if zop_matches:
        print(f"找到 {len(zop_matches)} 条data-zop数据\n")

        for i, zop_str in enumerate(zop_matches[:3], 1):
            # 解码HTML实体
            zop_str = html.unescape(zop_str)
            try:
                zop_data = json.loads(zop_str)
                print(f"样本 {i}:")
                print(json.dumps(zop_data, indent=2, ensure_ascii=False))
                print("-" * 80)
            except:
                print(f"样本 {i}: (解析失败)")
                print(zop_str[:200])
                print("-" * 80)

    # 2. 提取完整的回答卡片HTML结构
    print("\n【2. 回答卡片HTML结构样本】")

    # 查找ContentItem块
    card_pattern = r'<div[^>]*class="[^"]*ContentItem[^"]*"[^>]*>(.*?)</div>\s*(?=<div|</main|$)'
    cards = re.findall(card_pattern, content, re.DOTALL)

    if cards:
        print(f"找到 {len(cards)} 个内容卡片")
        print("\n第一个卡片的HTML结构(前500字符):")
        print("-" * 80)
        sample_card = cards[0][:500]
        # 格式化显示
        sample_card = re.sub(r'(</div>|<br/?>)', r'\1\n', sample_card)
        sample_card = re.sub(r'<(div|span|p|a|h[1-6])[^>]*>', r'\n<\1>', sample_card)
        print(sample_card)
        print("-" * 80)

    # 3. 提取作者信息HTML
    print("\n【3. 作者信息HTML结构】")
    author_pattern = r'<div[^>]*class="[^"]*AuthorInfo[^"]*"[^>]*>(.*?)</div>'
    authors = re.findall(author_pattern, content, re.DOTALL)

    if authors:
        print(f"找到 {len(authors)} 个作者信息块")
        print("\n第一个作者的HTML结构(前400字符):")
        print("-" * 80)
        print(re.sub(r'(</div>|<a|</a>)', r'\1\n', authors[0][:400]))
        print("-" * 80)

    # 4. 提取标题
    print("\n【4. 问题标题提取】")
    title_pattern = r'<h\d[^>]*class="[^"]*ContentItem-title[^"]*"[^>]*>(.*?)</h\d>'
    titles = re.findall(title_pattern, content, re.DOTALL | re.IGNORECASE)

    if titles:
        print(f"找到 {len(titles)} 个标题\n")
        for i, title in enumerate(titles[:5], 1):
            # 清理标题
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            clean_title = html.unescape(clean_title)
            print(f"{i}. {clean_title}")

    # 5. 提取文本内容
    print("\n【5. 回答正文文本样本】")
    content_pattern = r'<div[^>]*class="[^"]*RichContent[^"]*"[^>]*>(.*?)</div>'
    rich_contents = re.findall(content_pattern, content, re.DOTALL)

    if rich_contents:
        print(f"找到 {len(rich_contents)} 个富文本块")
        print("\n第一个回答的前200字符文本:")
        print("-" * 80)
        text = re.sub(r'<[^>]+>', '', rich_contents[0])
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:200])
        print("-" * 80)

    # 6. 提取链接模式
    print("\n【6. 完整链接样本】")
    link_pattern = r'href="(https://www\.zhihu\.com/(?:question|people)/[^"]+)"'
    links = re.findall(link_pattern, content)

    if links:
        unique_links = list(set(links))
        print(f"找到 {len(links)} 个链接 (去重: {len(unique_links)})")
        print("\n前10个链接:")
        for i, link in enumerate(unique_links[:10], 1):
            print(f"{i}. {link}")

    # 7. 检查懒加载和分页
    print("\n【7. 分页和加载机制】")

    # 查找分页按钮
    pagination = re.search(r'(下一页|加载更多|LoadMore|Pagination)', content, re.IGNORECASE)
    if pagination:
        print(f"✓ 发现分页/加载更多机制: {pagination.group(0)}")

    # 查找滚动加载
    infinite = re.search(r'(scroll.*load|infinite|lazy.*load)', content, re.IGNORECASE)
    if infinite:
        print(f"✓ 可能存在滚动加载: {infinite.group(0)}")

    # 查找API端点
    api_pattern = r'(https://api\.zhihu\.com/[^"\s]+|/api/[^"\s]+)'
    apis = re.findall(api_pattern, content)
    if apis:
        print(f"✓ 发现API端点: {len(set(apis))}个")
        for api in list(set(apis))[:5]:
            print(f"   - {api}")

    print("\n" + "=" * 100)

if __name__ == '__main__':
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'
    extract_samples(html_file)
