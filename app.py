# app.py
import streamlit as st
import subprocess
import sys
import model11_module
import time

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
if 'running' not in st.session_state:
    st.session_state.running = False
if 'uxplay_process' not in st.session_state:
    st.session_state.uxplay_process = None

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

    col3, col4 = st.columns(2)
    with col3:
        if not st.session_state.running and st.button("📷 START DETECTION", key="start", use_container_width=True):
            try:
                st.session_state.uxplay_process = subprocess.Popen(["/usr/local/bin/uxplay"])
            except Exception as e:
                st.warning(f"Failed to launch UXPlay: {e}")
            st.session_state.running = True

    with col4:
        if st.button("🔴 STOP", key="stop", use_container_width=True):
            st.session_state.running = False
            if st.session_state.uxplay_process:
                st.session_state.uxplay_process.terminate()
                st.session_state.uxplay_process = None

    frame_spot = st.empty()
    if st.session_state.running:
        for frame in model11_module.run_detection_yield_frames():
            frame_spot.image(frame, channels="RGB")
            if not st.session_state.running:
                break
            time.sleep(0.05)

    col_exit, col_results = st.columns(2)
    with col_exit:
        if st.button("⬅️ EXIT", key="exit", use_container_width=True):
            st.session_state.page = 'home'
    with col_results:
        if st.button("📊 RESULTS", key="results", use_container_width=True):
            st.session_state.page = 'results'

# === Results Page ===
def results_page():
    import plotly.graph_objects as go

    # Sample data
    ripe, unripe, overripe = 12, 8, 5
    total = ripe + unripe + overripe
    ripe_pct = (ripe / total) * 100 if total else 0
    unripe_pct = (unripe / total) * 100 if total else 0
    overripe_pct = (overripe / total) * 100 if total else 0

    st.markdown("<div class='overlay'><h2>DETECTION RESULTS</h2></div>", unsafe_allow_html=True)

    gap_ratio = 0.3
    col1, col_gap, col2 = st.columns([1, gap_ratio, 1])

    with col1:
        st.markdown(f"""
            <div style='background-color: #2e2e2e; padding: 20px 30px; border-radius: 12px; color: white;'>
                <h3>🍍 Maturity Breakdown</h3>
                <p><span style="color:limegreen;">🟢 Ripe:</span> {ripe_pct:.1f}%</p>
                <p><span style="color:orange;">🟠 Unripe:</span> {unripe_pct:.1f}%</p>
                <p><span style="color:crimson;">🔴 Overripe:</span> {overripe_pct:.1f}%</p>
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
