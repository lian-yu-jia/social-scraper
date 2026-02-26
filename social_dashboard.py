# social_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings

# Ignore the harmless Streamlit ScriptRunContext warning
warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# ------------------------
# Check if CSV exists
# ------------------------
csv_path = "data/master_social_data_clean.csv"

if not os.path.exists(csv_path):
    st.error(f"❌ CSV file not found at {csv_path}. Please make sure it exists.")
    st.stop()

# ------------------------
# Load CSV
# ------------------------
df = pd.read_csv(csv_path)

# Ensure all numeric columns exist
for col in ['views', 'likes', 'comments', 'shares']:
    if col not in df.columns:
        df[col] = 0

# Convert numeric columns to float safely
df[['views','likes','comments','shares']] = df[['views','likes','comments','shares']].fillna(0).astype(float)

# ------------------------
# Page Settings
# ------------------------
st.set_page_config(page_title="Social Media Dashboard", layout="wide")
st.title("📊 Social Media Analytics Dashboard")
st.markdown("Week 2 Prototype: Combined YouTube, Instagram & TikTok Metrics")

# ------------------------
# Filters
# ------------------------
platforms = df['platform'].unique().tolist()
selected_platforms = st.multiselect(
    "Select platforms to display:", 
    platforms, 
    default=platforms
)

filtered_df = df[df['platform'].isin(selected_platforms)].copy()  # copy to avoid warnings

# ------------------------
# Total Metrics by Platform
# ------------------------
st.subheader("Total Engagement Metrics by Platform")
metrics = filtered_df.groupby('platform')[['views','likes','comments','shares']].sum().reset_index()
st.dataframe(metrics)

# ------------------------
# Charts
# ------------------------
st.subheader("Views Comparison")
fig_views = px.bar(
    metrics, x='platform', y='views', text='views', color='platform', 
    labels={'views':'Total Views', 'platform':'Platform'}
)
st.plotly_chart(fig_views, use_container_width=True)

st.subheader("Likes Comparison")
fig_likes = px.bar(
    metrics, x='platform', y='likes', text='likes', color='platform',
    labels={'likes':'Total Likes', 'platform':'Platform'}
)
st.plotly_chart(fig_likes, use_container_width=True)

st.subheader("Comments Comparison")
fig_comments = px.bar(
    metrics, x='platform', y='comments', text='comments', color='platform',
    labels={'comments':'Total Comments', 'platform':'Platform'}
)
st.plotly_chart(fig_comments, use_container_width=True)

st.subheader("Shares Comparison")
fig_shares = px.bar(
    metrics, x='platform', y='shares', text='shares', color='platform',
    labels={'shares':'Total Shares', 'platform':'Platform'}
)
st.plotly_chart(fig_shares, use_container_width=True)

# ------------------------
# Top Posts Leaderboard
# ------------------------
st.subheader("🏆 Top Posts by Engagement")
filtered_df['total_engagement'] = filtered_df[['views','likes','comments','shares']].sum(axis=1)
top_posts = filtered_df.sort_values('total_engagement', ascending=False).head(10)
st.dataframe(top_posts[['platform','url','caption','views','likes','comments','shares','total_engagement']])

# ------------------------
# Detailed Post Table
# ------------------------
st.subheader("All Scraped Posts")
st.dataframe(filtered_df[['platform','url','caption','views','likes','comments','shares','status']])

# ------------------------
# Download Cleaned CSV
# ------------------------
st.subheader("Download Cleaned Data")
st.download_button(
    label="📥 Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="master_social_data_filtered.csv",
    mime="text/csv"
)
