import pandas as pd
import os
import re

files = ["data/youtube_data.csv", "data/instagram_data.csv", "data/tiktok_data.csv"]

dfs = []
for f in files:
    if os.path.exists(f):
        df = pd.read_csv(f)
        if 'platform' not in df.columns:
            df['platform'] = os.path.basename(f).split('_')[0]

        expected_cols = ['platform', 'url', 'caption', 'views', 'likes', 'comments', 'shares', 'status']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        dfs.append(df)

master_df = pd.concat(dfs, ignore_index=True)

# New convert_number function that extracts numeric part
def convert_number(s):
    if s is None or pd.isna(s):
        return 0
    s = str(s).replace(',', '').upper().strip()

    # Extract the numeric part using regex
    match = re.search(r'[\d\.]+', s)
    if not match:
        return 0

    num = float(match.group())

    if 'M' in s:
        num *= 1_000_000
    elif 'K' in s:
        num *= 1_000

    return num

# Apply conversion safely
for col in ['views', 'likes', 'comments', 'shares']:
    master_df[col] = master_df[col].apply(convert_number)

master_df.to_csv("data/master_social_data_clean.csv", index=False)
print("✅ Clean master CSV created: data/master_social_data_clean.csv")
