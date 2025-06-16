import streamlit as st

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
        margin-top: 100px;
        border-radius: 12px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    .overlay h1, .overlay h2, .overlay p {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# === Page State ===
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# === Home Page ===
def home_page():
    st.markdown("""
        <style>
        .home-overlay {
            position: relative;
            height: 80vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .connect-button-container {
            position: absolute;
            top: 35%;
            left: 55%;
            transform: translate(-50%, -50%);
            text-align: center;
        }

        .connect-button-container button {
            font-size: 22px !important;
            padding: 10px 40px !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title (can float above or stay at top)
    st.markdown("""
        <div class="overlay">
            <h1>Computer Vision-Based Drone Pineapple Maturity Detection:<br>Fuzzy Logic and YOLO</h1>
        </div>
    """, unsafe_allow_html=True)

    # Button positioned lower and right
    st.markdown('<div class="home-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="connect-button-container">', unsafe_allow_html=True)

    if st.button("Connect", use_container_width=False):
        st.session_state.page = "about"

    st.markdown('</div></div>', unsafe_allow_html=True)

# === About Page ===
def about_page():
    st.markdown("""
        <div class="overlay">
            <h2>HOW IT WORKS:</h2>
    """, unsafe_allow_html=True)

    instructions = [
        "1.) Download the DJI fly app and connect the drone to your device.",
        "2.) Press the start button to begin the pineapple maturity detection.",
        "3.) Press the stop button to end the pineapple maturity detection.",
        "4.) Press the result button to view the results and press exit to quit."
    ]

    cols = st.columns(2)
    for i, text in enumerate(instructions):
        cols[i % 2].markdown(f"<p style='color:white;'>{text}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START", key="start_from_about", use_container_width=True):
            st.session_state.page = 'control'

# === Control Panel Page ===
def control_panel():
    st.markdown("""
        <div class="overlay">
            <h2>CONTROL PANEL</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("START", key="start", use_container_width=True):
            st.success("START button clicked")
        if st.button("EXIT", key="exit", use_container_width=True):
            st.session_state.page = 'home'

    with col2:
        if st.button("STOP", key="stop", use_container_width=True):
            st.warning("STOP button clicked")
        if st.button("RESULTS", key="results", use_container_width=True):
            st.session_state.page = 'results'

# === Results Page ===
def results_page():
    st.markdown("""
        <div class="overlay">
            <h2>RESULTS</h2>
            <div style='display: flex; justify-content: space-around; padding-top: 20px;'>
                <div style='background-color: gray; padding: 30px; width: 30%; border-radius: 8px;'>
                    <h2 style='color:white;'>RIPE</h2>
                </div>
                <div style='background-color: gray; padding: 30px; width: 30%; border-radius: 8px;'>
                    <h2 style='color:white;'>UNRIPE</h2>
                </div>
                <div style='background-color: gray; padding: 30px; width: 30%; border-radius: 8px;'>
                    <h2 style='color:white;'>OVERRIPE</h2>
                </div>
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
