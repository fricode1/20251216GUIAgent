import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth


async def main():
    async with async_playwright() as p:
        # 使用持久化上下文，保存登录状态
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./chrome_profile",  # 保存session的目录
            headless=False,
            channel="chrome"  # 使用系统安装的Chrome
        )

        # 检查是否已有页面，没有则创建
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        stealth(page)

        await page.goto('https://www.zhihu.com/collection/19928423')

        print("浏览器已打开，请在浏览器中手动登录...")
        print("登录完成后，按回车键继续...")
        input()  # 等待用户按回车

        await page.screenshot(path='example-chromium.png')
        print("截图已保存")

        # 爬取页面内容
        print("\n开始爬取页面内容...")

        # 方法1：获取页面文本内容
        page_text = await page.text_content('body')
        print("\n=== 页面文本内容 ===")
        print(page_text[:500])  # 只打印前500个字符

        # 方法2：获取特定元素内容（根据实际页面结构调整选择器）
        # 例如获取文章标题
        # titles = await page.query_selector_all('.Card-item .ContentItem-title')
        # for i, title in enumerate(titles):
        #     title_text = await title.text_content()
        #     print(f"{i+1}. {title_text}")

        # 方法2.5：获取所有 data-za-detail-view-element_name="Title" 的内容
        titles = await page.evaluate('''() => {
            const elements = document.querySelectorAll('[data-za-detail-view-element_name="Title"]');
            return Array.from(elements).map(el => ({
                text: el.innerText,
                href: el.href || '',
                tagName: el.tagName
            }));
        }''')

        print(f"\n=== 找到 {len(titles)} 个标题 ===")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title['text']}")
            if title['href']:
                print(f"   链接: {title['href']}")

        # 保存到文件
        with open('zhihu_titles.txt', 'w', encoding='utf-8') as f:
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title['text']}\n")
                if title['href']:
                    f.write(f"   链接: {title['href']}\n")
                f.write("\n")
        print("\n标题已保存到 zhihu_titles.txt")

        # 爬取每个链接的详细内容
        print("\n" + "="*50)
        print("开始爬取每个回答的详细内容...")
        print("="*50)
        print("提示：如果遇到限制，可以:")
        print("1. 增加延迟时间（修改sleep参数）")
        print("2. 使用已登录的浏览器session")
        print("3. 手动访问几个页面后再运行")
        print("="*50)

        all_content = []
        for i, title in enumerate(titles, 1):
            if not title['href']:
                continue

            print(f"\n[{i}/{len(titles)}] 正在爬取: {title['text'][:50]}...")
            try:
                # 创建新页面访问链接
                article_page = await browser.new_page()
                stealth(article_page)

                # 模拟真实用户行为 - 慢速滚动加载
                await article_page.goto(title['href'], wait_until='domcontentloaded', timeout=30000)

                # 等待页面完全加载
                await asyncio.sleep(2)

                # 检查是否被限制
                is_blocked = await article_page.evaluate('''() => {
                    return document.body.innerText.includes('暂时限制本次访问') ||
                           document.body.innerText.includes('验证') ||
                           document.body.innerText.includes('异常');
                }''')

                if is_blocked:
                    print(f"   ❌ 触发反爬虫限制，跳过此链接")
                    await article_page.close()
                    # 增加延迟时间
                    await asyncio.sleep(5)
                    continue

                # 等待内容加载
                try:
                    await article_page.wait_for_selector('article', timeout=10000)
                except:
                    print(f"   ⚠️  超时，尝试继续提取内容...")

                # 模拟人工滚动
                await article_page.evaluate('window.scrollTo(0, document.body.scrollHeight/3)')
                await asyncio.sleep(1)
                await article_page.evaluate('window.scrollTo(0, document.body.scrollHeight/2)')
                await asyncio.sleep(1)

                # 提取内容
                content = await article_page.evaluate('''() => {
                    // 获取回答内容
                    const answerContent = document.querySelector('.RichContent-inner') ||
                                         document.querySelector('article') ||
                                         document.querySelector('.Post-RichText');

                    // 获取作者信息
                    const author = document.querySelector('.AuthorInfo-name')?.innerText ||
                                  document.querySelector('.UserLink-link')?.innerText ||
                                  '未知作者';

                    // 获取点赞数
                    const votes = document.querySelector('.VoteButton--up')?.innerText ||
                                 '0';

                    return {
                        author: author,
                        votes: votes,
                        content: answerContent ? answerContent.innerText.substring(0, 3000) : '无法获取内容'
                    };
                }''')

                all_content.append({
                    'title': title['text'],
                    'url': title['href'],
                    'author': content['author'],
                    'votes': content['votes'],
                    'content': content['content']
                })

                print(f"   ✅ 作者: {content['author']}")
                print(f"   点赞: {content['votes']}")
                print(f"   内容长度: {len(content['content'])} 字符")

                await article_page.close()

                # 随机延迟，模拟真实用户行为（3-6秒）
                import random
                delay = random.uniform(3, 6)
                print(f"   等待 {delay:.1f} 秒...")
                await asyncio.sleep(delay)

            except Exception as e:
                print(f"   ❌ 爬取失败: {str(e)}")
                # 出错后增加延迟
                await asyncio.sleep(5)
                continue

        # 保存所有内容到文件
        print("\n" + "="*50)
        print("保存所有内容到文件...")
        print("="*50)

        with open('zhihu_articles.txt', 'w', encoding='utf-8') as f:
            for i, article in enumerate(all_content, 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"文章 {i}\n")
                f.write(f"{'='*80}\n")
                f.write(f"标题: {article['title']}\n")
                f.write(f"链接: {article['url']}\n")
                f.write(f"作者: {article['author']}\n")
                f.write(f"点赞: {article['votes']}\n")
                f.write(f"\n内容:\n{article['content']}\n")
                f.write(f"\n{'='*80}\n\n")

        print(f"\n已保存 {len(all_content)} 篇文章到 zhihu_articles.txt")

        # 方法3：获取页面完整HTML
        page_html = await page.content()
        with open('zhihu_page.html', 'w', encoding='utf-8') as f:
            f.write(page_html)
        print("\nHTML已保存到 zhihu_page.html")

        # 方法4：使用evaluate执行JavaScript获取数据
        # items = await page.evaluate('''() => {
        #     return Array.from(document.querySelectorAll('.Card-item')).map(item => ({
        #         title: item.querySelector('.ContentItem-title')?.innerText,
        #         author: item.querySelector('.AuthorInfo-name')?.innerText
        #     }))
        # }''')
        # print(f"\n获取到 {len(items)} 个内容项")
        # for item in items:
        #     print(f"- {item['title']} by {item['author']}")

        await browser.close()

asyncio.run(main())