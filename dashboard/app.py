import pandas as pd
import streamlit as st
import os

st.title("YouTube Video Stats Dashboard")

CSV_FILE = "data/youtube.csv"

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    st.write("Latest data:")
    st.dataframe(df)

    # Select video to plot
    video_ids = df["video_id"].unique()
    selected_video = st.selectbox("Select video", video_ids)

    video_df = df[df["video_id"] == selected_video].sort_values("date")
    st.line_chart(video_df[["views", "likes"]].set_index(video_df["date"]))
else:
    st.warning("No data found. Run youtube_scraper.py first.")
