from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import re


def parse_number(text):
    if not text:
        return 0
    text = text.replace(",", "").strip()
    if "K" in text:
        return int(float(text.replace("K", "").replace("likes", "").strip()) * 1000)
    if "M" in text:
        return int(float(text.replace("M", "").replace("likes", "").strip()) * 1_000_000)
    return int(re.findall(r"\d+", text)[0])


def scrape_instagram_post(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        time.sleep(10)  # let Instagram fully load

        # Caption (best effort, first meaningful text)
        try:
            caption = page.locator("article div span").first.inner_text()
        except:
            caption = ""

        # Likes (new method)
        likes = 0
        try:
            likes_text = page.locator("section span").filter(has_text="likes").first.inner_text()
            likes = parse_number(likes_text)
        except:
            pass

        # Comments count (estimate)
        try:
            comments_count = page.locator("ul ul").count()
        except:
            comments_count = 0

        browser.close()

        return {
            "url": url,
            "caption": caption,
            "likes": likes,
            "comments_count": comments_count,
            "status": "success"
        }


if __name__ == "__main__":

    URL_FILE = "url/insta_url.txt"
    OUTPUT_FILE = "data/instagram_data.csv"

    if not os.path.exists(URL_FILE):
        print("❌ Instagram URL file not found")
        exit()

    urls = open(URL_FILE).read().splitlines()
    results = []

    for url in urls:
        print(f"📸 Scraping Instagram: {url}")
        try:
            results.append(scrape_instagram_post(url))
        except Exception as e:
            results.append({
                "url": url,
                "caption": "",
                "likes": 0,
                "comments_count": 0,
                "status": "failed"
            })
            print(f"⚠️ Failed: {e}")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)

    print("✅ Instagram automatic scraping completed")
