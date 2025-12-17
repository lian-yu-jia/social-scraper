from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_tiktok(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        views = page.locator("strong[data-e2e='video-views']").inner_text()
        likes = page.locator("strong[data-e2e='like-count']").inner_text()

        browser.close()

        return {
            "url": url,
            "views": views,
            "likes": likes
        }
