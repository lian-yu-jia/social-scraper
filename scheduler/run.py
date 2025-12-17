import schedule
import time
import os

def run_all():
    os.system("python scrapers/youtube_scraper.py")
    os.system("python scrapers/tiktok_scraper.py")

schedule.every().day.at("02:00").do(run_all)

while True:
    schedule.run_pending()
    time.sleep(60)
