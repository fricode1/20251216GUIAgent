#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析知乎收藏夹HTML文件"""

import re
import sys
from html import unescape
from collections import Counter
import json

# 设置stdout编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {
        'questions': set(),
        'answers': set(),
        'authors': set(),
        'vote_counts': [],
        'comment_counts': [],
        'titles': [],
        'urls': set()
    }

    # 提取问题ID
    questions = re.findall(r'question/(\d+)', content)
    results['questions'] = list(set(questions))

    # 提取回答ID
    answers = re.findall(r'answer/(\d+)', content)
    results['answers'] = list(set(answers))

    # 提取作者信息
    authors = re.findall(r'//www\.zhihu\.com/people/([^/"\s]+)', content)
    results['authors'] = list(set(authors))

    # 提取标题
    titles = re.findall(r'<h\d[^>]*>([^<]+)</h\d>', content, re.IGNORECASE)
    titles += re.findall(r'title="([^"]{20,150})"', content)
    results['titles'] = list(set([unescape(t.strip()) for t in titles if len(t.strip()) > 10]))[:20]

    # 提取数值(可能是赞同数/评论数)
    numbers = re.findall(r'(\d{1,2},?\d{3})', content)
    results['vote_counts'] = list(set(numbers))[:30]

    # 提取URL
    urls = re.findall(r'https?://[^\s"<>\']+', content)
    results['urls'] = [u for u in set(urls) if 'zhihu.com' in u and 'question' in u][:20]

    return results

def main():
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'

    print("=" * 80)
    print("知乎收藏夹页面分析报告")
    print("=" * 80)

    results = extract_data(html_file)

    print(f"\n[统计概览]")
    print(f"   - 问题数量: {len(results['questions'])}")
    print(f"   - 回答数量: {len(results['answers'])}")
    print(f"   - 作者数量: {len(results['authors'])}")

    print(f"\n[问题ID列表 (前10个)]:")
    for i, qid in enumerate(results['questions'][:10], 1):
        print(f"   {i}. {qid}")

    print(f"\n[回答ID列表 (前10个)]:")
    for i, aid in enumerate(results['answers'][:10], 1):
        print(f"   {i}. {aid}")

    print(f"\n[作者列表 (前10个)]:")
    for i, author in enumerate(results['authors'][:10], 1):
        print(f"   {i}. {author}")

    print(f"\n[相关URL链接]:")
    for i, url in enumerate(results['urls'], 1):
        print(f"   {i}. {url}")

    print(f"\n[提取的标题]:")
    for i, title in enumerate(results['titles'][:10], 1):
        print(f"   {i}. {title}")

    print(f"\n[爬取建议]:")
    print("   [可爬取的内容]:")
    print("      1. 问题标题和描述")
    print("      2. 回答内容(正文)")
    print("      3. 作者信息(昵称、简介)")
    print("      4. 互动数据(赞同数、评论数、收藏数)")
    print("      5. 时间戳(创建/编辑时间)")
    print("      6. 标签和话题")
    print("      7. 相关推荐内容")

    print("\n   [注意事项]:")
    print("      - 知乎有反爬虫机制,需控制频率")
    print("      - 部分内容可能需要登录")
    print("      - 遵守robots.txt和服务条款")
    print("      - 数据仅供学习研究使用")

if __name__ == '__main__':
    main()
