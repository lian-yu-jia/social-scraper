import yt_dlp
import pandas as pd

def scrape_youtube_video(url):
    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "views": info.get("view_count"),
        "publish_date": info.get("upload_date"),
        "channel": info.get("uploader"),
        "url": url
    }

urls = open("url/youtube_url.txt").read().splitlines()
data = []

for url in urls:
    data.append(scrape_youtube_video(url))

pd.DataFrame(data).to_csv("data/youtube_data.csv", index=False)
print("✅ YouTube auto-scraping completed")
