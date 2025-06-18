import streamlit as st
import subprocess
import sys

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

# === Page State ===
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'input_mode' not in st.session_state:
    st.session_state.input_mode = "Live (UX Play)"  # Default selection

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

    st.markdown("<div style='text-align: center;'><h4 style='color:white;'>Choose Input Mode:</h4></div>", unsafe_allow_html=True)

    # Initialize selected mode
    if 'input_mode' not in st.session_state:
        st.session_state.input_mode = "Live (UX Play)"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Live (UX Play)", use_container_width=True):
            st.session_state.input_mode = "Live (UX Play)"
    with col2:
        if st.button("Test Video", use_container_width=True):
            st.session_state.input_mode = "Test Video"

    # Highlight selected input mode
    selected_mode = st.session_state.input_mode
    st.markdown(
        f"""
        <style>
        .highlight-container {{
            display: flex;
            justify-content: center;
            margin-top: 10px;
            gap: 20px;
        }}
        .highlight-box {{
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            color: white;
        }}
        .selected {{
            background-color: #00cc66;
        }}
        .unselected {{
            background-color: #555;
        }}
        </style>
        <div class="highlight-container">
            <div class="highlight-box {'selected' if selected_mode == 'Live (UX Play)' else 'unselected'}">Live (UX Play)</div>
            <div class="highlight-box {'selected' if selected_mode == 'Test Video' else 'unselected'}">Test Video</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col3, col4 = st.columns(2)
    with col3:
        if st.button("START", key="start", use_container_width=True):
            try:
                if selected_mode == "Live (UX Play)":
                    subprocess.Popen(["C:\\Path\\To\\uxplay.exe"])  # Adjust path
                    subprocess.Popen([sys.executable, "model11.py", "live"])
                else:
                    subprocess.Popen([sys.executable, "model11.py", "test"])
                st.success(f"✅ Detection started using {selected_mode}!")
            except FileNotFoundError as e:
                st.error(f"❌ Failed to start: {e}")

        if st.button("EXIT", key="exit", use_container_width=True):
            st.session_state.page = 'home'

    with col4:
        if st.button("STOP", key="stop", use_container_width=True):
            st.warning("🛑 Manually close or press 'q' in the OpenCV window.")
        if st.button("RESULTS", key="results", use_container_width=True):
            st.session_state.page = 'results'

# === Results Page ===
def results_page():
    st.markdown("""
        <div class='overlay'>
            <h2>RESULTS</h2>
            <div style='display: flex; justify-content: space-around;'>
                <div style='background-color: gray; padding: 30px; border-radius: 8px;'><h2 style='color:white;'>RIPE</h2></div>
                <div style='background-color: gray; padding: 30px; border-radius: 8px;'><h2 style='color:white;'>UNRIPE</h2></div>
                <div style='background-color: gray; padding: 30px; border-radius: 8px;'><h2 style='color:white;'>OVERRIPE</h2></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
