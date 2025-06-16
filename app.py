import streamlit as st

# Page state management
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# === Home Page ===
def home_page():
    # Inject real background image via CSS using your GitHub-hosted image
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://github.com/SHERWIN092702/pineapple-drone-app/blob/main/background.jpg?raw=true");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .overlay-box {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 30px;
            border-radius: 10px;
            max-width: 800px;
            margin: 100px auto 30px auto;
        }
        .title-text {
            color: white;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            line-height: 1.5;
        }
        .button-container {
            text-align: center;
            margin-top: 40px;
        }
        .button-container button {
            font-size: 24px;
            padding: 10px 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Overlay title and button content
    st.markdown("<div class='overlay-box'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='title-text'>"
        "Computer Vision-Based Drone Pineapple Maturity Detection:<br>Fuzzy Logic and YOLO"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("Connect"):
        st.session_state.page = "about"
    st.markdown("</div>", unsafe_allow_html=True)

# === About Page ===
def about_page():
    st.image("background.jpg", use_container_width=True)
    st.markdown("<h2 style='color: white;'>HOW IT WORKS:</h2>", unsafe_allow_html=True)

    instructions = [
        "1.) Download the DJI fly app and connect the drone to your device.",
        "2.) Press the start button to begin the pineapple maturity detection.",
        "3.) Press the stop button to end the pineapple maturity detection.",
        "4.) Press the result button to view the results and press exit to quit."
    ]

    cols = st.columns(2)
    for i, text in enumerate(instructions):
        cols[i % 2].markdown(f"<p style='color:white; font-size:18px;'>{text}</p>", unsafe_allow_html=True)

    if st.button("START", key="start_from_about"):
        st.session_state.page = 'control'

# === Control Panel Page ===
def control_panel():
    st.image("background.jpg", use_container_width=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("START", key="start"):
            st.success("START button clicked")
        if st.button("EXIT", key="exit"):
            st.session_state.page = 'home'

    with col2:
        if st.button("STOP", key="stop"):
            st.warning("STOP button clicked")
        if st.button("RESULTS", key="results"):
            st.session_state.page = 'results'

# === Results Page ===
def results_page():
    st.image("background.jpg", use_container_width=True)
    st.markdown("""
        <div style='display: flex; justify-content: space-around; padding-top: 20px;'>
            <div style='background-color: gray; padding: 30px; width: 30%;'>
                <h2 style='color:white;'>RIPE</h2>
            </div>
            <div style='background-color: gray; padding: 30px; width: 30%;'>
                <h2 style='color:white;'>UNRIPE</h2>
            </div>
            <div style='background-color: gray; padding: 30px; width: 30%;'>
                <h2 style='color:white;'>OVERRIPE</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("EXIT", key="exit_results"):
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
