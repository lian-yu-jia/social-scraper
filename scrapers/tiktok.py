from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re
import os


def scrape_tiktok_video(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        time.sleep(8)

        # Scroll to trigger stats load
        page.mouse.wheel(0, 3000)
        time.sleep(3)

        # Get all <strong> texts
        raw_stats = page.locator("strong").all_inner_texts()

        # Keep only values that look like numbers (e.g. 3.4M, 16K)
        stats = [s for s in raw_stats if re.search(r"\d", s)]

        views = stats[0] if len(stats) > 0 else None
        likes = stats[1] if len(stats) > 1 else None
        comments = stats[2] if len(stats) > 2 else None
        shares = stats[3] if len(stats) > 3 else None

        browser.close()

        status = "success" if views or likes else "partial_success"

        return {
            "url": url,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "status": status
        }


if __name__ == "__main__":

    URL_FILE = "url/tiktok_url.txt"
    OUTPUT_FILE = "data/tiktok_data.csv"

    if not os.path.exists(URL_FILE):
        print("❌ TikTok URL file not found")
        exit()

    urls = open(URL_FILE).read().splitlines()
    results = []

    for url in urls:
        print(f"Scraping: {url}")
        try:
            data = scrape_tiktok_video(url)
            results.append(data)
        except Exception as e:
            results.append({
                "url": url,
                "views": None,
                "likes": None,
                "comments": None,
                "shares": None,
                "status": "failed"
            })
            print(f"⚠️ Failed: {e}")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)

    print("✅ TikTok automatic scraping completed")
