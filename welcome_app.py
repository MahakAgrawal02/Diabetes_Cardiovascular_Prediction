import streamlit as st
from PIL import Image
import base64
import os

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = None

# # Function to toggle theme
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# Function to set selected module
def select_module(module):
    st.session_state.selected_module = module

# Function to get image as base64 string
def get_img_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Page Config
st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🏥",
    layout="wide"
)

# Load CSS based on theme
theme = st.session_state.theme
# icon_path = f"assets/icons/{'moon' if theme == 'light' else 'sun'}.png"
heartbeat_icon = get_img_as_base64("assets/icons/heartbeat.png")
diabetes_icon = get_img_as_base64("assets/icons/disease_icon/diabetes.png")
heart_icon = get_img_as_base64("assets/icons/disease_icon/heart.png")

# Define CSS
css = f"""
<style>
    /* Base Styles */
    :root {{
        --background-color: {('#ffffff' if theme == 'light' else '#1e1e1e')};
        --text-color: {('#333333' if theme == 'light' else '#f0f0f0')};
        --accent-color: #3498db;
        --card-bg: {('#f8f9fa' if theme == 'light' else '#2d2d2d')};
        --card-border: {('#e6e6e6' if theme == 'light' else '#3d3d3d')};
        --card-shadow: {('0 4px 6px rgba(0, 0, 0, 0.1)' if theme == 'light' else '0 4px 6px rgba(0, 0, 0, 0.3)')};
        --hover-bg: {('#e9f7fe' if theme == 'light' else '#373737')};
        --button-bg: #3498db;
        --button-text: white;
    }}

    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
    }}

    /* Header Styles */
    .header {{
        display: flex;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid var(--card-border);
        margin-bottom: 2rem;
    }}

    .header-title {{
        flex-grow: 1;
        text-align: center;
    }}

    /* Disease Card Styles */
    .card-container {{
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }}

    .disease-card {{
        background-color: var(--card-bg);
        border-radius: 10px;
        border: 1px solid var(--card-border);
        padding: 20px;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }}

    .disease-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        background-color: var(--hover-bg);
    }}

    .disease-card.selected {{
        border: 2px solid var(--accent-color);
        background-color: var(--hover-bg);
    }}

    .card-icon {{
        width: 60px;
        height: 60px;
        object-fit: contain;
        margin-bottom: 15px;
    }}

    .card-title {{
        font-size: 1.3rem;
        margin-bottom: 10px;
        color: var(--accent-color);
    }}

    .card-description {{
        font-size: 0.9rem;
        color: var(--text-color);
        line-height: 1.5;
    }}

    /* Theme Toggle Button */
    .theme-toggle {{
        cursor: pointer;
        padding: 5px;
        border-radius: 50%;
        background-color: var(--card-bg);
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }}

    .theme-toggle:hover {{
        background-color: var(--hover-bg);
    }}

    /* Style for select buttons under cards */
    button[data-testid="diabetes-select-button"],
    button[data-testid="cardio-select-button"] {{
        font-weight: bold !important;
        color: var(--text-color) !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        height: 100% !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        opacity: 0 !important;
        cursor: pointer !important;
    }}

    /* Launch Button */
    .launch-button {{
        background-color: var(--primary-dark) !important;
        color: var(--text-color);
        font-weight: bold !important;
        padding: 12px 24px;
        border-radius: 30px;
        border: none;
        cursor: pointer;
        display: block;
        margin: 0 auto;
        width: fit-content;
        transition: all 0.3s ease;
        opacity: {('1' if st.session_state.selected_module else '0.5')};
        pointer-events: {('all' if st.session_state.selected_module else 'none')};
    }}

    .launch-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        color: white !important;
        background-color: var(--primary-dark) !important;
    }}

    /* Footer */
    .footer {{
        margin-top: 50px;
        text-align: center;
        padding: 20px;
        font-size: 0.8rem;
        color: var(--text-color);
        opacity: 0.7;
        border-top: 1px solid var(--card-border);
    }}

    /* Hide Streamlit elements */
    #MainMenu {{display: none;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Custom header with theme toggle
st.markdown(f"""
<div class="header">
    <div style="width:80px;">
        <img src="data:image/png;base64,{heartbeat_icon}" width="60">
    </div>
    <div class="header-title">
        <h1>HealthGuard AI</h1>
        <p>Multi-Disease Risk Prediction Platform</p>
    </div>
    <div class="theme-toggle" onclick="
        const form = window.parent.document.querySelector('form.stButton button[kind=formSubmit]');
        if (form) {{ form.click(); }}
    ">
        <img src="assets/icons/{'moon' if theme == 'light' else 'sun'}.png" width="24">
    </div>
</div>
""", unsafe_allow_html=True)

# Hidden button for theme toggle JavaScript to click
# st.button("Toggle Theme", on_click=toggle_theme, key="theme_toggle_button", help="Toggle dark/light mode", args=None)

# Disease Selection Cards
st.markdown("## 🔍 Select Prediction Module")

# Create two columns for the cards
col1, col2 = st.columns(2)

# Selected class for styling
diabetes_selected = "selected" if st.session_state.selected_module == "diabetes" else ""
cardio_selected = "selected" if st.session_state.selected_module == "cardio" else ""
# Diabetes card
with col1:
    diabetes_card = st.container()
    diabetes_card.markdown(f"""
    <div class="disease-card {diabetes_selected}" style="position: relative;">
        <img src="data:image/png;base64,{diabetes_icon}" class="card-icon">
        <h3 class="card-title">Diabetes Risk</h3>
        <p class="card-description">Predict your likelihood of developing Type 2 Diabetes based on health markers and lifestyle factors.</p>
    </div>
    """, unsafe_allow_html=True)
    # Hidden button for JavaScript to click
    st.button("Select Diabetes", on_click=select_module, key="diabetes-select-button", args=("diabetes",), help="Select Diabetes Module")

# Cardiovascular card
with col2:
    cardio_card = st.container()
    cardio_card.markdown(f"""
    <div class="disease-card {cardio_selected}" style="position: relative;">
        <img src="data:image/png;base64,{heart_icon}" class="card-icon">
        <h3 class="card-title">Cardiovascular Risk</h3>
        <p class="card-description">Assess your risk of heart disease and stroke using clinically validated risk factors and biomarkers.</p>
    </div>
    """, unsafe_allow_html=True)
    # Hidden button for JavaScript to click
    st.button("Select Cardio", on_click=select_module, key="cardio-select-button", args=("cardio",), help="Select Cardiovascular Module")
# Display selected module info
if st.session_state.selected_module:
    st.success(f"✅ You've selected the {st.session_state.selected_module.title()} Risk Module")

# Launch Button - Using Markdown for custom styling
st.markdown(f"""
<button class="launch-button" onclick="
    const launchBtn = window.parent.document.querySelector('button[data-testid=\\"launch-button\\"]');
    if (launchBtn) {{ launchBtn.click(); }}
">
    Launch {st.session_state.selected_module.title() if st.session_state.selected_module else "Selected"} Module 🚀
</button>
""", unsafe_allow_html=True)

# Hidden launch button for JavaScript to click
if st.button("Launch", key="launch-button", help="Launch Selected Module"):
    if st.session_state.selected_module == 'diabetes':
        os.system("streamlit run diabetes_app.py")
    elif st.session_state.selected_module == 'cardio':
        os.system("streamlit run cardiovascular_app.py")

# Features section
st.markdown("## ✨ Key Features")
feature_cols = st.columns(3)
with feature_cols[0]:
    st.markdown("""
    ### 🔬 Evidence-Based
    Models trained on extensive clinical datasets and validated against published research.
    """)
with feature_cols[1]:
    st.markdown("""
    ### 🛡️ Privacy-Focused
    Your health data never leaves your device; all processing happens locally.
    """)
with feature_cols[2]:
    st.markdown("""
    ### 📊 Actionable Insights
    Receive personalized recommendations based on your unique risk factors.
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2023 HealthGuard AI | Clinical decision support system</p>
    <p>This application is for educational purposes only and should not replace professional medical advice</p>
</div>
""", unsafe_allow_html=True)