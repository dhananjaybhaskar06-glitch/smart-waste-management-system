import streamlit as st
import pandas as pd
import sqlite3
import subprocess
import folium
from datetime import datetime

from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

import plotly.express as px
import plotly.graph_objects as go

from dashboard.components import load_theme
from dashboard.locations import BIN_COORDINATES
from prediction.predictor import predict_fill_levels
from route_optimizer import get_collection_route

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Waste Command Center",
    page_icon="🗑",
    layout="wide"
)

load_theme()

st_autorefresh(interval=5000, key="refresh")

# =====================================================
# HEADER (PREMIUM UI)
# =====================================================

st.markdown("""
<div style='text-align:center'>
<h1>🗑 Smart City Waste Intelligence Platform</h1>
<h4 style='color:gray'>Real-Time IoT Monitoring • AI Prediction • GIS Analytics</h4>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("⚙ Control Panel")

st.sidebar.markdown(
f"🕒 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.info("""
🏙 Smart City Command Center Active  
✔ 10 Smart Bins  
✔ AI Prediction Engine  
✔ Route Optimization  
✔ GIS Mapping  
✔ Real-Time Alerts  
""")

# =====================================================
# LOAD DATA
# =====================================================

DB_PATH = "data/waste_management.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("SELECT * FROM waste_data", conn)

conn.close()

if df.empty:
    st.warning("No data found. Run simulator first.")
    st.stop()

# =====================================================
# LATEST DATA
# =====================================================

latest = (
    df.sort_values("timestamp")
    .groupby("bin_id")
    .tail(1)
)

# =====================================================
# KPI METRICS
# =====================================================

total_bins = len(latest)
critical_bins = len(latest[latest["priority"] == "URGENT"])
avg_fill = round(latest["fill_percentage"].mean(), 2)
alerts = len(latest[latest["alert"] == "YES"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Bins", total_bins)

with c2:
    st.metric("Avg Fill %", avg_fill)

with c3:
    st.metric("Critical Bins", critical_bins)

with c4:
    st.metric("Alerts", alerts)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Analytics",
    "🗺 Map & Routes",
    "📄 Reports"
])

# =====================================================
# TAB 1 - OVERVIEW
# =====================================================

with tab1:

    st.subheader("🚨 Active Alerts")

    critical = latest[latest["alert"] == "YES"]

    if critical.empty:
        st.success("No active alerts")
    else:
        st.dataframe(critical, use_container_width=True)

    st.subheader("🔥 Priority Bins")

    st.dataframe(
        latest.sort_values("fill_percentage", ascending=False),
        use_container_width=True
    )

# =====================================================
# TAB 2 - ANALYTICS
# =====================================================

with tab2:

    st.subheader("📈 Waste Trend")

    fig = px.line(
        df,
        x="timestamp",
        y="fill_percentage",
        color="bin_id"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🥧 Status Distribution")

    status_df = latest["status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]

    pie = px.pie(
        status_df,
        values="Count",
        names="Status",
        hole=0.4
    )

    st.plotly_chart(pie, use_container_width=True)

    st.subheader("🤖 AI Prediction")

    predictions = predict_fill_levels()

    if predictions:
        pred_df = pd.DataFrame(
            list(predictions.items()),
            columns=["Bin", "Predicted Fill %"]
        )

        st.dataframe(pred_df, use_container_width=True)

# =====================================================
# TAB 3 - MAP & ROUTE
# =====================================================

with tab3:

    st.subheader("🗺 Smart Bin Map")

    m = folium.Map(location=[28.615, 77.045], zoom_start=13)

    for _, row in latest.iterrows():

        coords = BIN_COORDINATES.get(row["bin_id"])

        if coords:

            folium.Marker(
                coords,
                popup=f"""
                <b>{row['bin_id']}</b><br>
                {row['location']}<br>
                Fill: {row['fill_percentage']}%<br>
                Status: {row['status']}
                """
            ).add_to(m)

    st_folium(m, width=1200, height=500)

    st.subheader("🚚 Optimized Collection Route")

    route = get_collection_route(latest)

    st.dataframe(route, use_container_width=True)

# =====================================================
# TAB 4 - REPORTS
# =====================================================

with tab4:

    st.subheader("📄 Reports Center")

    if st.button("Generate PDF Report"):

        subprocess.run(["python", "reports/pdf_report.py"])

        st.success("PDF Report Generated Successfully")

    st.download_button(
        "⬇ Download CSV Data",
        df.to_csv(index=False),
        "waste_data.csv",
        "text/csv"
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
---
<center>
Smart Waste Management System  
Built with Python • Streamlit • AI • IoT Simulation • GIS
</center>
""", unsafe_allow_html=True)