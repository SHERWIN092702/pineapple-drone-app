# app.py with results pie chart using detection count file

import streamlit as st
import subprocess
import sys
import time
import os
import plotly.graph_objects as go
import json
from pathlib import Path

# === Global CSS Background + Styling ===
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://github.com/SHERWIN092702/pineapple-drone-app/blob/main/background.jpg?raw=true");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .overlay {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 40px;
        border-radius: 12px;
        color: white;
        margin: 40px auto;
        max-width: 800px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# === Page State Initialization ===
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'uxplay_proc' not in st.session_state:
    st.session_state.uxplay_proc = None
if 'detection_proc' not in st.session_state:
    st.session_state.detection_proc = None
if 'stream_mode' not in st.session_state:
    st.session_state.stream_mode = 'UXPlay'
if 'rtmp_url' not in st.session_state:
    st.session_state.rtmp_url = ''

# === Home Page ===
def home_page():
    st.markdown("<div class='overlay'><h1>Drone Pineapple Maturity Detection</h1></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔌 Connect", use_container_width=True):
            st.session_state.page = "about"

# === About Page ===
def about_page():
    st.markdown("<div class='overlay'><h2>HOW IT WORKS:</h2></div>", unsafe_allow_html=True)
    instructions = [
        "1. Download the DJI Fly app and connect the drone.",
        "2. Press START to begin detection.",
        "3. Press STOP to end detection.",
        "4. Press RESULTS to view output. Press EXIT to quit."
    ]
    cols = st.columns(2)
    for i, text in enumerate(instructions):
        cols[i % 2].markdown(f"<p style='color:white;'>{text}</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START", key="start_from_about", use_container_width=True):
            st.session_state.page = 'control'

# === Control Panel Page ===
def control_panel():
    st.markdown("<div class='overlay'><h2>CONTROL PANEL</h2></div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Stream source selector
    st.session_state.stream_mode = st.selectbox("Select Video Source:", ["UXPlay", "RTMP Stream"], index=0)

    if st.session_state.stream_mode == "RTMP Stream":
        st.session_state.rtmp_url = st.text_input("Enter RTMP Stream URL (e.g. from DJI Fly):", value=st.session_state.rtmp_url)

    col3, col4 = st.columns(2)
    with col3:
        if st.button("📷 START DETECTION", key="start", use_container_width=True):
            try:
                detection_script = "/home/rpi5/Desktop/yolo_object/model11.py"

                subprocess.run(["pkill", "uxplay"])

                # Only launch UXPlay if selected
                if st.session_state.stream_mode == "UXPlay":
                    uxplay_path = "/usr/local/bin/uxplay"
                    uxplay_proc = subprocess.Popen([uxplay_path])
                    st.session_state.uxplay_proc = uxplay_proc

                # Launch detection
                detection_proc = subprocess.Popen([sys.executable, detection_script])
                st.session_state.detection_proc = detection_proc

                st.success("✅ Detection started!" + (" Using UXPlay." if st.session_state.stream_mode == "UXPlay" else " Using RTMP Stream."))

            except Exception as e:
                st.error(f"❌ Failed to start: {e}")

        if st.button("⬅️ EXIT", key="exit", use_container_width=True):
            try:
                if st.session_state.detection_proc:
                    st.session_state.detection_proc.terminate()
                    st.session_state.detection_proc = None
                if st.session_state.uxplay_proc:
                    st.session_state.uxplay_proc.terminate()
                    st.session_state.uxplay_proc = None
                subprocess.run(["pkill", "uxplay"])
            except Exception as e:
                st.error(f"⚠️ Failed to stop: {e}")
            st.session_state.page = 'home'

    with col4:
        if st.button("🔴 STOP", key="stop", use_container_width=True):
            try:
                if st.session_state.detection_proc:
                    st.session_state.detection_proc.terminate()
                    st.session_state.detection_proc = None
                if st.session_state.uxplay_proc:
                    st.session_state.uxplay_proc.terminate()
                    st.session_state.uxplay_proc = None
                subprocess.run(["pkill", "uxplay"])
                st.success("🛑 Detection stopped.")
            except Exception as e:
                st.error(f"⚠️ Failed to stop: {e}")

        if st.button("📊 RESULTS", key="results", use_container_width=True):
            try:
                if st.session_state.detection_proc:
                    st.session_state.detection_proc.terminate()
                    st.session_state.detection_proc = None
                if st.session_state.uxplay_proc:
                    st.session_state.uxplay_proc.terminate()
                    st.session_state.uxplay_proc = None
                subprocess.run(["pkill", "uxplay"])
            except Exception as e:
                st.error(f"⚠️ Failed to stop: {e}")
            st.session_state.page = 'results'

# === Results Page ===
def results_page():
    st.markdown("<div class='overlay'><h2>DETECTION RESULTS</h2></div>", unsafe_allow_html=True)

    counts_file = Path("/home/rpi5/Desktop/yolo_object/detection_counts.json")
    counts = {"ripe": 0, "unripe": 0, "overripe": 0}
    if counts_file.exists():
        with open(counts_file) as f:
            counts = json.load(f)

    ripe = counts["ripe"]
    unripe = counts["unripe"]
    overripe = counts["overripe"]
    total = ripe + unripe + overripe

    if total == 0:
        st.warning("No detection data found yet. Run the detection first to see results.")
        return

    ripe_pct = (ripe / total) * 100
    unripe_pct = (unripe / total) * 100
    overripe_pct = (overripe / total) * 100

    gap_ratio = 0.3
    col1, col_gap, col2 = st.columns([1, gap_ratio, 1])

    with col1:
        st.markdown(f"""
            <div style='background-color: #2e2e2e; padding: 20px 30px; border-radius: 12px; color: white;'>
                <h3>🍍 Maturity Breakdown</h3>
                <p><span style=\"color:limegreen;\">🟢 Ripe:</span> {ripe_pct:.1f}%</p>
                <p><span style=\"color:orange;\">🟠 Unripe:</span> {unripe_pct:.1f}%</p>
                <p><span style=\"color:crimson;\">🔴 Overripe:</span> {overripe_pct:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=['Ripe', 'Unripe', 'Overripe'],
            values=[ripe, unripe, overripe],
            marker=dict(colors=['limegreen', 'orange', 'crimson']),
            hole=0.3,
            textinfo='label+percent'
        )])
        fig.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            width=300,
        )
        st.plotly_chart(fig, use_container_width=False)

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("⬅️ BACK TO CONTROL", key="exit_results", use_container_width=True):
            try:
                if st.session_state.detection_proc:
                    st.session_state.detection_proc.terminate()
                    st.session_state.detection_proc = None
                if st.session_state.uxplay_proc:
                    st.session_state.uxplay_proc.terminate()
                    st.session_state.uxplay_proc = None
                subprocess.run(["pkill", "uxplay"])
            except Exception as e:
                st.error(f"⚠️ Failed to stop: {e}")
            st.session_state.page = 'control'

# === Page Router ===
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'about':
    about_page()
elif st.session_state.page == 'control':
    control_panel()
elif st.session_state.page == 'results':
    results_page()
