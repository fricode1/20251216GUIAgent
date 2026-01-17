#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""深入分析知乎页面结构"""

import re
import sys
from html import unescape
from collections import defaultdict, Counter
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_structure(html_file):
    """分析HTML结构"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    analysis = {
        'meta_tags': [],
        'css_classes': Counter(),
        'data_attributes': Counter(),
        'script_patterns': [],
        'json_data': [],
        'dom_structure': defaultdict(list)
    }

    print("=" * 100)
    print("知乎收藏夹页面 - 结构深度分析")
    print("=" * 100)

    # 1. Meta标签分析
    print("\n【1. Meta标签信息】")
    meta_tags = re.findall(r'<meta[^>]+>', content, re.IGNORECASE)
    print(f"   发现 {len(meta_tags)} 个meta标签")

    for tag in meta_tags[:10]:
        name = re.search(r'name=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        prop = re.search(r'property=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        content_match = re.search(r'content=["\']([^"\']{0,80})["\']', tag, re.IGNORECASE)

        if name:
            print(f"   - name: {name.group(1)}")
            if content_match:
                print(f"     content: {content_match.group(1)}")
        elif prop:
            print(f"   - property: {prop.group(1)}")
            if content_match:
                print(f"     content: {content_match.group(1)}")

    # 2. CSS类名分析
    print("\n【2. 主要CSS类名】")
    css_classes = re.findall(r'class=["\']([^"\']{5,40})["\']', content)
    css_counter = Counter(css_classes)
    for cls, count in css_counter.most_common(20):
        print(f"   .{cls} ({count}次)")

    # 3. Data属性分析
    print("\n【3. Data-* 属性】")
    data_attrs = re.findall(r'data-([a-z-]+)=["\']', content, re.IGNORECASE)
    data_counter = Counter(data_attrs)
    for attr, count in data_counter.most_common(15):
        print(f"   data-{attr} ({count}次)")

    # 4. JavaScript数据模式
    print("\n【4. JavaScript数据模式】")

    # 查找JSON数据
    json_patterns = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({[^;]+});', content)
    if json_patterns:
        print(f"   ✓ 发现 __INITIAL_STATE__ ({len(json_patterns)}处)")
        try:
            data = json.loads(json_patterns[0])
            print(f"   - 顶层keys: {list(data.keys())[:10]}")
        except:
            print(f"   - 解析失败,数据长度: {len(json_patterns[0])} 字符")
    else:
        print("   ✗ 未发现 __INITIAL_STATE__")

    # 查找其他数据模式
    patterns = [
        ('data-zop-feedlist', r'data-zop-feedlist=["\']([^"\']+)["\']'),
        ('data-zop', r'data-zop=["\']([^"\']+)["\']'),
        ('data-za-element-id', r'data-za-element-id=["\']([^"\']+)["\']'),
        ('data-za-module', r'data-za-module=["\']([^"\']+)["\']'),
    ]

    for name, pattern in patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"   ✓ {name}: {len(matches)}处")
            if matches:
                print(f"     示例: {matches[0][:100]}")

    # 5. DOM结构分析
    print("\n【5. DOM结构层级】")

    # 统计主要容器
    containers = {
        'div': len(re.findall(r'<div[^>]*>', content)),
        'a': len(re.findall(r'<a[^>]+>', content)),
        'span': len(re.findall(r'<span[^>]*>', content)),
        'p': len(re.findall(r'<p[^>]*>', content)),
        'h1-h3': len(re.findall(r'<h[1-3][^>]*>', content)),
        'img': len(re.findall(r'<img[^>]+>', content)),
        'script': len(re.findall(r'<script[^>]*>', content)),
        'link': len(re.findall(r'<link[^>]+>', content)),
    }

    for tag, count in containers.items():
        print(f"   <{tag}>: {count}个")

    # 6. URL模式分析
    print("\n【6. URL模式分析】")
    url_patterns = {
        '问题链接': r'//www\.zhihu\.com/question/\d+',
        '回答链接': r'//www\.zhihu\.com/question/\d+/answer/\d+',
        '用户链接': r'//www\.zhihu\.com/people/[^/"\s]+',
        '专栏链接': r'//zhuanlan\.zhihu\.com/p/\d+',
        '话题链接': r'//www\.zhihu\.com/topic/\d+',
    }

    for name, pattern in url_patterns.items():
        matches = re.findall(pattern, content)
        unique_matches = list(set(matches))
        print(f"   {name}: {len(matches)}个 (去重: {len(unique_matches)}个)")
        if unique_matches:
            print(f"     示例: {unique_matches[0]}")

    # 7. 反爬虫特征分析
    print("\n【7. 反爬虫特征检测】")

    anti_bot_features = {
        'nonce属性': r'<script[^>]*nonce=["\'][^"\']+["\']',
        '内联混淆脚本': r'<script[^>]*>!function',
        '样式指纹': r'data-emotion-css',
        '性能监控': r'web-reporter|sentry|crash',
        'webpack打包': r'webpackJsonp|__webpack_require__',
        'React根节点': r'data-reactroot|data-react-checksum',
    }

    for name, pattern in anti_bot_features.items():
        if re.search(pattern, content, re.IGNORECASE):
            print(f"   ✓ {name}: 检测到")
        else:
            print(f"   ✗ {name}: 未检测到")

    # 8. 数据加载方式
    print("\n【8. 数据加载方式分析】")

    # 检测SSR vs CSR
    initial_content = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if initial_content:
        body_length = len(initial_content.group(1))
        script_blocks = len(re.findall(r'<script[^>]*>.*?</script>', content, re.DOTALL))
        inline_data = len(re.findall(r'window\.__\w+__', content))

        print(f"   - Body内容长度: {body_length:,} 字符")
        print(f"   - Script标签数量: {script_blocks}")
        print(f"   - 内联数据对象: {inline_data}")

        if body_length > 50000:
            print(f"   → 推测: 服务端渲染(SSR)为主")
        else:
            print(f"   → 推测: 客户端渲染(CSR)为主")

    # 9. 关键选择器
    print("\n【9. 关键CSS选择器建议】")

    selectors = {
        '问题标题': [
            '.QuestionHeader-main',
            '.QuestionHeader-title',
            'h1.QuestionHeader-title',
        ],
        '回答列表': [
            '.List-item',
            '.AnswerCard',
            '[data-zop-feedlist]',
        ],
        '作者信息': [
            '.AuthorInfo-name',
            '.UserLink-link',
            '[data-za-element-id="Author"]',
        ],
        '赞同数': [
            '.VoteButton',
            '.VoteButton--up',
            '[data-za-element-id="Vote"]',
        ],
        '评论按钮': [
            '.ContentItem-actions',
            '.Button--plain',
            '[data-za-element-id="Comment"]',
        ],
    }

    for element, sels in selectors.items():
        print(f"\n   {element}:")
        for sel in sels:
            exists = "✓" if re.search(re.escape(sel).replace('\\*', '[^"\']*'), content) else " "
            print(f"     {exists} {sel}")

    # 10. 爬虫建议
    print("\n【10. 爬虫开发建议】")
    print("\n   推荐方案:")
    print("   1. 使用Selenium/Playwright模拟真实浏览器")
    print("   2. 等待页面完全加载后再提取数据")
    print("   3. 优先使用data-*属性定位元素(更稳定)")
    print("   4. 设置合理的User-Agent和Referer")
    print("   5. 控制请求频率(2-5秒间隔)")
    print("   6. 使用Cookie池/代理池(如有需要)")
    print("   7. 考虑使用官方API(需要逆向分析)")

    print("\n   关键数据位置:")
    print("   - window.__INITIAL_STATE__: 包含页面初始数据")
    print("   - data-zop-feedlist: Feed流数据")
    print("   - data-za-*: 埋点数据,可用于定位元素")

    print("\n" + "=" * 100)

if __name__ == '__main__':
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'
    analyze_structure(html_file)
