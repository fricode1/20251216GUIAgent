"""
电影网站爬虫 - 爬取 https://ssr2.scrape.center/page/1
使用 Playwright 提取电影列表信息
"""
import asyncio
import csv
import json
from playwright.async_api import async_playwright


async def scrape_movies(page_num=1):
    """爬取指定页码的电影数据"""
    base_url = f"https://ssr2.scrape.center/page/{page_num}"
    movies = []

    async with async_playwright() as p:
        # 启动浏览器（使用非无头模式以便调试）
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print(f"正在访问: {base_url}")
        await page.goto(base_url, wait_until="networkidle")

        # 等待电影列表加载
        await page.wait_for_selector(".el-card.item")

        # 获取所有电影卡片
        movie_cards = await page.locator(".el-card.item").all()

        print(f"找到 {len(movie_cards)} 部电影")

        for idx, card in enumerate(movie_cards, 1):
            try:
                # 提取电影信息
                # 电影名称
                name = await card.locator("h2.m-b-sm").text_content()

                # 封面图片URL
                cover_url = await card.locator("img.cover").get_attribute("src")

                # 类别
                category_elements = await card.locator(".categories .el-button.category span").all()
                categories = [await cat.text_content() for cat in category_elements]

                # 地区和时长
                info_text = await card.locator(".info").first.text_content()
                info_parts = info_text.split(" / ")
                region = info_parts[0].strip() if len(info_parts) > 0 else ""
                duration = info_parts[1].strip() if len(info_parts) > 1 else ""

                # 上映日期
                release_date_elem = await card.locator(".info").all()
                if len(release_date_elem) > 1:
                    release_date = await release_date_elem[1].text_content()
                    release_date = release_date.replace(" 上映", "").strip()
                else:
                    release_date = ""

                # 评分
                score = await card.locator("p.score").text_content()

                # 详情页链接
                detail_link = await card.locator("a.name").get_attribute("href")
                detail_url = f"https://ssr2.scrape.center{detail_link}" if detail_link else ""

                movie_data = {
                    "序号": idx,
                    "名称": name.strip() if name else "",
                    "类别": ", ".join(categories),
                    "地区": region,
                    "时长": duration,
                    "上映日期": release_date,
                    "评分": score.strip() if score else "",
                    "封面": cover_url,
                    "详情页": detail_url
                }

                movies.append(movie_data)
                print(f"[{idx}] {name.strip()} - {score}")

            except Exception as e:
                print(f"提取第 {idx} 部电影时出错: {str(e)}")
                continue

        await browser.close()

    return movies


async def save_to_csv(movies, filename="movies.csv"):
    """保存数据到CSV文件"""
    if not movies:
        print("没有数据需要保存")
        return

    keys = movies[0].keys()

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(movies)

    print(f"数据已保存到 {filename}")


async def save_to_json(movies, filename="movies.json"):
    """保存数据到JSON文件"""
    if not movies:
        print("没有数据需要保存")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到 {filename}")


async def main():
    """主函数"""
    print("=" * 60)
    print("电影网站爬虫启动")
    print("=" * 60)

    # 爬取第1页
    movies = await scrape_movies(page_num=1)

    print(f"\n共爬取到 {len(movies)} 部电影")

    # 保存数据
    await save_to_csv(movies, "movies.csv")
    await save_to_json(movies, "movies.json")

    print("\n爬取完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
