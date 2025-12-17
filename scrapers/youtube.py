import pandas as pd
from googleapiclient.discovery import build
import os
from datetime import date

# --- CONFIG ---
API_KEY = "AIzaSyCT7KxgmkHQW3cvTdddDlQJYtKN3ohhmdg"
VIDEO_IDS = ["FN2CdB60yZw"]  # Add more video IDs here
CSV_FILE = "data/youtube.csv"

os.makedirs("data", exist_ok=True)

# --- BUILD API CLIENT ---
youtube = build('youtube', 'v3', developerKey=API_KEY)

rows = []

for video_id in VIDEO_IDS:
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    
    if response["items"]:
        item = response["items"][0]
        title = item["snippet"]["title"]
        views = int(item["statistics"].get("viewCount", 0))
        likes = int(item["statistics"].get("likeCount", 0))
        publish_date = item["snippet"]["publishedAt"][:10]

        rows.append({
            "date": str(date.today()),
            "video_id": video_id,
            "title": title,
            "views": views,
            "likes": likes,
            "publish_date": publish_date
        })
    else:
        print(f"No data for video: {video_id}")

# --- SAVE TO CSV ---
if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE)
    df = pd.concat([df_existing, pd.DataFrame(rows)], ignore_index=True)
else:
    df = pd.DataFrame(rows)

df.to_csv(CSV_FILE, index=False)
print("✅ YouTube data saved to CSV")

