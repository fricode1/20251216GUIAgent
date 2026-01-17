#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""可视化页面DOM结构"""

import re
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def visualize_dom_structure(html_file):
    """可视化DOM树结构"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 100)
    print("知乎页面 - DOM结构可视化")
    print("=" * 100)

    print("\n【整体结构】\n")
    print("""
    <html>
    │
    ├─<head>
    │  ├─ <meta> (239个)
    │  ├─ <link> (27个样式表)
    │  └─ <script> (监控、配置脚本)
    │
    └─<body>
       │
       ├─ 顶部导航栏
       │  └─ .css-s8xum0 (固定头部)
       │
       ├─ 主内容区
       │  │
       │  └─ 收藏夹内容容器
       │     │
       │     └─ [回答卡片 1]
       │        │
       │        ├─ .ContentItem-title (问题标题)
       │        │  └─ <a> 问题链接
       │        │     └─ data-zop (JSON元数据)
       │        │
       │        ├─ .AuthorInfo (作者信息)
       │        │  ├─ .AuthorInfo-avatarWrapper (头像)
       │        │  ├─ .AuthorInfo-name (姓名)
       │        │  └─ .AuthorInfo-detail (简介/徽章)
       │        │
       │        ├─ .RichContent (正文内容)
       │        │  ├─ .RichContent-inner (正文)
       │        │  └─ .ContentItem-arrowIcon (展开按钮)
       │        │
       │        └─ .ContentItem-actions (操作栏)
       │             ├─ .VoteButton (赞同)
       │             ├─ .Button (评论)
       │             └─ .Button (收藏)
       │
       │     └─ [回答卡片 2-19] (重复上述结构)
       │
       └─ 侧边栏/其他元素
    """)

    print("\n【关键元素层级关系】\n")
    print("""
    1. 回答卡片定位
       └─ .ContentItem.AnswerItem
          └─ [data-zop] ← 最稳定的定位方式!

    2. 问题标题
       └─ .ContentItem-title
          └─ <a itemprop="url">
             └─ 文本内容

    3. 作者信息
       └─ .AuthorInfo
          ├─ meta[itemprop="name"] ← 结构化数据
          ├─ meta[itemprop="image"]
          ├─ .UserLink.AuthorInfo-avatarWrapper
          │  └─ <img> 头像
          └─ .UserLink.AuthorInfo-name
             └─ <a> 作者链接

    4. 正文内容
       └─ .RichContent.is-collapsed (默认折叠)
          └─ .RichContent-inner
             └─ <p> 段落内容

    5. 互动按钮
       └─ .ContentItem-actions
          ├─ .VoteButton (赞同)
          ├─ [data-za-element-id="Comment"] (评论)
          └─ [data-za-element-id="Collection"] (收藏)
    """)

    print("\n【数据流向】\n")
    print("""
    用户请求
        ↓
    服务器渲染HTML
        ↓
    ┌──────────────────┐
    │  包含主要内容   │
    │  (SSR)          │
    └──────────────────┘
        ↓
    浏览器接收HTML
        ↓
    ┌──────────────────┐
    │ 解析HTML构建DOM │
    └──────────────────┘
        ↓
    执行JavaScript
        ↓
    ┌──────────────────┐
    │ 绑定事件监听    │
    │ 加载额外资源    │
    └──────────────────┘
        ↓
    页面完全加载
        ↓
    用户可交互
    """)

    print("\n【选择器优先级】\n")
    print("""
    优先级1: data-* 属性 (最稳定)
    ├─ [data-zop]           ← 回答卡片
    ├─ [data-za-module]     ← 功能模块
    └─ [data-za-element-id] ← 具体元素

    优先级2: itemprop 语义化标签
    ├─ [itemprop="name"]    ← 标题/姓名
    ├─ [itemprop="url"]     ← 链接
    └─ [itemprop="image"]   ← 图片

    优先级3: BEM类名 (较稳定)
    ├─ .ContentItem
    ├─ .AuthorInfo
    ├─ .RichContent
    └─ .VoteButton

    优先级4: emotion动态类名 (不稳定)
    └─ .css-{hash} ← 避免使用!
    """)

    # 统计实际的嵌套层级
    print("\n【实际DOM深度分析】\n")

    # 提取一个完整的卡片结构
    card_pattern = r'<div[^>]*class="[^"]*ContentItem[^"]*"[^>]*>(.*?)</div>\s*(?=<div class="ContentItem|</main>|$)'
    cards = re.findall(card_pattern, content, re.DOTALL)

    if cards:
        sample = cards[0]

        # 统计标签嵌套
        lines = sample.split('>')
        depth = 0
        max_depth = 0
        tag_stack = []

        structure = []
        for line in lines[:50]:  # 只看前50行
            open_tags = re.findall(r'<([a-z][a-z0-9]*)\s', line, re.IGNORECASE)
            close_tags = re.findall(r'</([a-z][a-z0-9]*)>', line, re.IGNORECASE)

            for tag in open_tags:
                if tag not in ['br', 'hr', 'img', 'input']:
                    depth += 1
                    max_depth = max(max_depth, depth)
                    tag_stack.append(tag)
                    structure.append(f"{'  ' * depth}<{tag}>")

            for tag in close_tags:
                if tag_stack and tag_stack[-1] == tag:
                    tag_stack.pop()
                    depth -= 1
                    structure.append(f"{'  ' * (depth + 1)}</{tag}>")

        print(f"最大嵌套深度: {max_depth} 层")
        print("\n前50行DOM结构:")
        for line in structure[:30]:
            print(line)

    print("\n【爬虫数据提取路径】\n")
    print("""
    步骤1: 找到所有回答卡片
    soup.select('[data-zop]')
         ↓
    步骤2: 遍历每个卡片
    for card in cards:
         ↓
    步骤3: 提取data-zop JSON
    zop = json.loads(card['data-zop'])
         ↓
    步骤4: 提取标题
    title = card.select_one('.ContentItem-title a').text
         ↓
    步骤5: 提取作者
    author = card.select_one('.AuthorInfo-name').text
         ↓
    步骤6: 提取正文
    content = card.select_one('.RichContent-inner').text
         ↓
    步骤7: 提取链接
    url = card.select_one('a[itemprop="url"]')['content']
         ↓
    步骤8: 保存数据
    save_to_json/database
    """)

    print("\n" + "=" * 100)
    print("\n【总结】")
    print("""
    ✓ 页面结构清晰,符合HTML5语义化标准
    ✓ 使用data-*属性提供稳定的定位方式
    ✓ SSR渲染使得数据提取相对简单
    ✓ 主要内容都在HTML中,无需等待JS执行
    ⚠️ 注意动态类名(css-{hash})会变化
    ⚠️ 部分内容可能需要展开/滚动加载
    """)
    print("=" * 100)

if __name__ == '__main__':
    html_file = r'c:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\GUI_Agent效果录屏\实验66：反爬工具调研\collection_page.html'
    visualize_dom_structure(html_file)
