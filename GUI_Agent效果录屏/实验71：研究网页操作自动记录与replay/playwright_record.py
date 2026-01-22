import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www.baidu.com/")
    page.get_by_role("textbox", name="内蒙古党委书记:成立调查组").click()
    page.get_by_role("textbox", name="内蒙古党委书记:成立调查组").fill("武林外传")
    page.get_by_role("button", name="百度一下").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="武林外传(电视剧)_CCTV节目官网-电视剧_央视网(").click()
    page1 = page1_info.value
    page1.get_by_role("link", name="2", exact=True).click()
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="《武林外传》 第28集").nth(1).click()
    page2 = page2_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
