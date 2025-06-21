import streamlit as st
import subprocess
import sys
import plotly.graph_objects as go

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

# === Home Page ===
def home_page():
    st.markdown("<div class='overlay'><h1>Drone Pineapple Maturity Detection</h1></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Connect", use_container_width=True):
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
        if st.button("START", key="start_from_about", use_container_width=True):
            st.session_state.page = 'control'

# === Control Panel Page ===
def control_panel():
    st.markdown("<div class='overlay'><h2>CONTROL PANEL</h2></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        if st.button("START", key="start", use_container_width=True):
            try:
                uxplay_path = "/usr/local/bin/uxplay"  # Change if installed elsewhere
                detection_script = "model11.py"         # Change if needed

                # Start uxplay
                uxplay_proc = subprocess.Popen([uxplay_path])
                st.session_state.uxplay_proc = uxplay_proc

                # Start detection script
                detection_proc = subprocess.Popen([sys.executable, detection_script])
                st.session_state.detection_proc = detection_proc

                st.success("✅ UXPlay and detection started!")

            except Exception as e:
                st.error(f"❌ Failed to start: {e}")

        if st.button("EXIT", key="exit", use_container_width=True):
            st.session_state.page = 'home'

    with col4:
        if st.button("STOP", key="stop", use_container_width=True):
            try:
                if st.session_state.detection_proc:
                    st.session_state.detection_proc.terminate()
                    st.session_state.detection_proc = None
                if st.session_state.uxplay_proc:
                    st.session_state.uxplay_proc.terminate()
                    st.session_state.uxplay_proc = None
                st.success("🛑 UXPlay and detection stopped.")
            except Exception as e:
                st.error(f"⚠️ Failed to stop: {e}")

        if st.button("RESULTS", key="results", use_container_width=True):
            st.session_state.page = 'results'

# === Results Page ===

def results_page():
    # Example data (you can replace this later with real detection values)
    ripe = 12
    unripe = 8
    overripe = 5
    total = ripe + unripe + overripe

    ripe_pct = (ripe / total) * 100 if total > 0 else 0
    unripe_pct = (unripe / total) * 100 if total > 0 else 0
    overripe_pct = (overripe / total) * 100 if total > 0 else 0

    st.markdown("<div class='overlay'><h2>DETECTION RESULTS</h2></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    # === Left: Percentages Panel ===
    with col1:
        st.markdown("""
            <div class='overlay'>
                <h3 style='color:white;'>🍍 Maturity Levels</h3>
                <p style='font-size:18px; color:lime;'>✅ Ripe: {:.1f}%</p>
                <p style='font-size:18px; color:orange;'>🟠 Unripe: {:.1f}%</p>
                <p style='font-size:18px; color:red;'>🔴 Overripe: {:.1f}%</p>
            </div>
        """.format(ripe_pct, unripe_pct, overripe_pct), unsafe_allow_html=True)

    # === Right: Pie Chart ===
    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=['Ripe', 'Unripe', 'Overripe'],
            values=[ripe, unripe, overripe],
            marker=dict(colors=['limegreen', 'orange', 'crimson']),
            hole=0.3,
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        fig.update_layout(
            title='Maturity Distribution',
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    # === Exit Button Centered ===
    col_exit = st.columns([1, 2, 1])[1]
    with col_exit:
        if st.button("EXIT", key="exit_results", use_container_width=True):
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
