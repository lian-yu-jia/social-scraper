import streamlit as st
import pandas as pd
import os

def tiktok_str_to_int(s):
    if s is None or s == "":
        return 0
    s = s.replace(",", "").strip()
    if s.endswith("M"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("K"):
        return int(float(s[:-1]) * 1_000)
    else:
        try:
            return int(s)
        except:
            return 0

def str_to_int(s):
    if s is None or s == "":
        return 0
    s = str(s).replace(",", "").strip()
    if s.endswith("M"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("K"):
        return int(float(s[:-1]) * 1_000)
    else:
        try:
            return int(s)
        except:
            return 0


# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    layout="wide"
)

st.title("📊 Social Media Analytics Dashboard")
st.caption("Internship Project · YouTube, Instagram & TikTok")

# ---------------------------------
# File Paths
# ---------------------------------
DATA_PATH = "data"

YT_FILE = os.path.join(DATA_PATH, "youtube_data.csv")
IG_FILE = os.path.join(DATA_PATH, "instagram_data.csv")
TT_FILE = os.path.join(DATA_PATH, "tiktok_data.csv")

# ---------------------------------
# Load Data Function
# ---------------------------------
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

yt_df = load_data(YT_FILE)
ig_df = load_data(IG_FILE)
tt_df = load_data(TT_FILE)

# ---------------------------------
# Sidebar – Dataset Status
# ---------------------------------
st.sidebar.header("📁 Dataset Status")

st.sidebar.write("YouTube:", "✅ Loaded" if not yt_df.empty else "❌ Not Found")
st.sidebar.write("Instagram:", "✅ Loaded" if not ig_df.empty else "❌ Not Found")
st.sidebar.write("TikTok:", "✅ Loaded" if not tt_df.empty else "❌ Not Found")

# ---------------------------------
# Tabs
# ---------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎥 YouTube Analytics",
    "📸 Instagram Analytics",
    "🎵 TikTok Analytics"
])

# =================================
# YouTube Tab
# =================================
with tab1:
    st.subheader("YouTube Overview")

    if yt_df.empty:
        st.warning("YouTube data not found. Run the YouTube scraper first.")
    else:
        col1, col2 = st.columns(2)

        col1.metric("Total Videos", len(yt_df))

        if "views" in yt_df.columns:
            col2.metric("Total Views", int(yt_df["views"].sum()))
        else:
            col2.metric("Total Views", "N/A")

        st.divider()

        st.subheader("YouTube Data")
        st.dataframe(yt_df, use_container_width=True)

        if "views" in yt_df.columns:
            st.subheader("Views per Video")
            st.bar_chart(yt_df["views"])

# =================================
# Instagram Tab
# =================================
with tab2:
    st.subheader("Instagram Overview")

    if ig_df.empty:
        st.warning("Instagram data not found. Run the Instagram scraper first.")
    else:
        col1, col2 = st.columns(2)

        col1.metric("Total Posts", len(ig_df))

        if "likes" in ig_df.columns:
            col2.metric("Total Likes", ig_df["likes"].astype(str).count())
        else:
            col2.metric("Total Likes", "N/A")

        if "likes" in ig_df.columns:
            ig_df["likes_int"] = ig_df["likes"].apply(str_to_int)

            avg_ig_likes = ig_df["likes_int"].mean()

            st.metric(
                "Average Likes (Instagram)",
                int(avg_ig_likes) if avg_ig_likes > 0 else "N/A"
            )
            

        st.divider()

        st.subheader("Instagram Data")
        st.dataframe(ig_df, use_container_width=True)

# =================================
# TikTok Tab
# =================================
with tab3:
    st.subheader("TikTok Overview")
    
    # Convert views to numbers
    if "views" in tt_df.columns:
        tt_df["views_int"] = tt_df["views"].apply(tiktok_str_to_int)

    


    if tt_df.empty:
        st.warning("TikTok data not found. Run the TikTok scraper first.")
    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Videos", len(tt_df))

        col2.metric(
            "Views",
            tt_df["views"].iloc[0] if "views" in tt_df.columns else "N/A"
        )
        col3.metric(
            "Likes",
            tt_df["likes"].iloc[0] if "likes" in tt_df.columns else "N/A"
        )
        col4.metric(
            "Comments",
            tt_df["comments"].iloc[0] if "comments" in tt_df.columns else "N/A"
        )

        if "likes" in tt_df.columns:
            tt_df["likes_int"] = tt_df["likes"].apply(str_to_int)

            avg_tt_likes = tt_df["likes_int"].mean()

            st.metric(
                "Average Likes (TikTok)",
                int(avg_tt_likes) if avg_tt_likes > 0 else "N/A"
            )

        st.divider()


        st.subheader("TikTok Data")
        st.dataframe(tt_df, use_container_width=True)
        st.subheader("Views per TikTok Video")
        st.bar_chart(tt_df["views_int"])

# ---------------------------------
# Footer
# ---------------------------------
st.divider()
st.caption("© Internship Project · Social Media Analytics Dashboard")
