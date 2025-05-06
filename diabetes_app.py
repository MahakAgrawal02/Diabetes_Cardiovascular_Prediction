import streamlit as st
import h2o
import pandas as pd
import base64

# Page Configuration
st.set_page_config(
    page_title="HealthGuard AI - Diabetes Prediction",
    page_icon="🏥",
    layout="wide"
)

# Add dark mode support at the VERY TOP of the CSS loading process
def inject_dark_css():
    try:
        with open("assets/css/dark.css", "r") as f:
            dark_css = f.read()
            st.markdown(f'<style>{dark_css}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Couldn't load dark mode CSS: {e}")

# Inject dark mode CSS FIRST
inject_dark_css()

# Initialize H2O
@st.cache_resource
def init_h2o():
    try:
        h2o.init()
        st.session_state.h2o_initialized = True
        return True
    except Exception as e:
        st.error(f"Failed to initialize H2O: {e}")
        return False

# Initialize H2O (this will only run once due to caching)
h2o_initialized = init_h2o()

# Function to get image as base64 string
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.warning(f"Couldn't load image from {file_path}: {e}")
        return ""

# Try to load theme icon
heartbeat_icon = get_img_as_base64("assets/icons/heartbeat.png")
diabetes_icon = get_img_as_base64("assets/icons/disease_icon/diabetes.png")
back_icon = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItYXJyb3ctbGVmdCI+PGxpbmUgeDE9IjE5IiB5MT0iMTIiIHgyPSI1IiB5Mj0iMTIiPjwvbGluZT48cG9seWxpbmUgcG9pbnRzPSIxMiAxOSA1IDEyIDEyIDUiPjwvcG9seWxpbmU+PC9zdmc+"

# Define CSS with theme-aware variables
css = """
<style>
    /* Theme-aware variables */
    :root {
        --primary: #3498db;
        --primary-dark: #2980b9;
        --secondary: #2ecc71;
        --accent: #9b59b6;
        --text: #f0f0f0;
        --background: #1e1e1e;
        --card: #2d2d2d;
        --card-border: #3d3d3d;
        --danger: #e74c3c;
        --warning: #f39c12;
        --info: #3498db;
        --success: #2ecc71;
    }

    /* Global styles */
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }

    /* Header */
    .header {
        display: flex;
        align-items: center;
        padding: 1rem;
        background-color: var(--card);
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .app-title {
        color: var(--primary);
        margin: 0;
        padding: 0;
    }

    .app-subtitle {
        color: var(--text);
        opacity: 0.8;
        margin-top: 0.5rem;
    }

    /* Form container */
    .form-container {
        background-color: var(--card);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }

    /* Section heading */
    .section-heading {
        color: var(--primary);
        font-size: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary);
    }

    /* Results container */
    .results-container {
        background-color: var(--card);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 2rem;
    }

    /* Status messages */
    .status-low {
        background-color: rgba(46, 204, 113, 0.1);
        color: var(--success);
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid var(--success);
    }

    .status-medium {
        background-color: rgba(243, 156, 18, 0.1);
        color: var(--warning);
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid var(--warning);
    }

    .status-high {
        background-color: rgba(231, 76, 60, 0.1);
        color: var(--danger);
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid var(--danger);
    }

    /* Keep all your other existing CSS rules below */
    /* Risk meter */
    .risk-meter {
        margin: 1.5rem 0;
    }

    .risk-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
    }

    .risk-low {
        color: var(--success);
    }

    .risk-medium {
        color: var(--warning);
    }

    .risk-high {
        color: var(--danger);
    }

    /* Custom select styles */
    div[data-baseweb="select"] {
        border-radius: 5px;
    }

    /* Custom slider styles */
    div[data-testid="stSlider"] > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Button styling */
    .stButton button {
        background-color: var(--primary);
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Back button */
    .back-button {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background-color: transparent;
        color: var(--text);
        border: 1px solid var(--card-border);
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        margin-bottom: 1rem;
    }

    .back-button:hover {
        background-color: rgba(0,0,0,0.05);
    }

    .back-button img {
        margin-right: 5px;
        width: 16px;
        height: 16px;
    }

    /* Progress bar override */
    div.stProgress > div > div > div > div {
        background-color: var(--primary);
    }

    /* Remove fullscreen option */
    button[title="View fullscreen"] {
        display: none;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Back button to welcome page
st.markdown(f"""
<a href="#" class="back-button" onclick="window.history.back()">
    <img src="{back_icon}"> Back to dashboard
</a>
""", unsafe_allow_html=True)

# Custom header
if heartbeat_icon:
    header_icon = f'<img src="data:image/png;base64,{heartbeat_icon}" width="60">'
else:
    header_icon = '🏥'

if diabetes_icon:
    diabetes_header_icon = f'<img src="data:image/png;base64,{diabetes_icon}" width="40" style="margin-right:10px;">'
else:
    diabetes_header_icon = '🩺'

st.markdown(f"""
<div class="header">
    <div style="margin-right: 20px;">
        {header_icon}
    </div>
    <div>
        <h1 class="app-title">HealthGuard AI - Diabetes Risk Assessment</h1>
        <p class="app-subtitle">Predict the likelihood of diabetes based on your health metrics</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Load MOJO model
@st.cache_resource
def load_model():
    try:
        return h2o.import_mojo("StackedEnsemble_AllModels_1_AutoML_1_20250331_161905.zip")
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

# Only try to load model if H2O initialized successfully
model = load_model() if h2o_initialized else None

# Rest of your existing code (input form, prediction logic, etc.) remains unchanged...
# [Input form, prediction processing, results display, etc.]

# Input form
st.markdown(f'<div class="section-heading">{diabetes_header_icon} Patient Details</div>', unsafe_allow_html=True)

with st.form("diabetes_prediction_form"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Create three columns for better organization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_bp = st.selectbox("High Blood Pressure", ["No", "Yes"], 
                              help="Has a doctor ever told you that you have high blood pressure?")
        bmi = st.slider("BMI", 10.0, 50.0, 25.0, 0.1, 
                       help="Body Mass Index (weight in kg / height in meters squared)")
        phys_hlth = st.slider("Physical Health Issues (Days/Month)", 0, 30, 0,
                             help="Number of days in the past 30 days when your physical health was not good")
    
    with col2:
        high_chol = st.selectbox("High Cholesterol", ["No", "Yes"], 
                                help="Has a doctor ever told you that you have high cholesterol?")
        smoker = st.selectbox("Heavy Alcohol Consumption", ["No", "Yes"],
                             help="More than 14 drinks per week for men or more than 7 drinks per week for women")
        ment_hlth = st.slider("Mental Health Issues (Days/Month)", 0, 30, 0,
                             help="Number of days in the past 30 days when your mental health was not good")
    
    with col3:
        chol_check = st.selectbox("Cholesterol Check in Last 5 Years", ["No", "Yes"],
                                 help="Have you had your cholesterol checked in the past 5 years?")
        phys_active = st.selectbox("Physical Activity", ["No", "Yes"],
                                  help="Do you engage in physical activities or exercises during a typical week?")
        gen_hlth = st.slider("General Health (1-5)", 1, 5, 3,
                            help="How would you rate your general health? (1=Excellent, 5=Poor)")
        
        diff_walk = st.selectbox("Difficulty Walking", ["No", "Yes"],
                               help="Do you have serious difficulty walking or climbing stairs?")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submitted = st.form_submit_button("Analyze Risk Factors")

# Process inputs and predict
if submitted:
    if model is None:
        st.error("Model could not be loaded. Please check the file path and try again.")
    else:
        # Convert inputs to model format
        input_dict = {
            "HighBP": 1 if high_bp == "Yes" else 0,
            "GenHlth": gen_hlth,
            "HighChol": 1 if high_chol == "Yes" else 0,
            "CholCheck": 1 if chol_check == "Yes" else 0,
            "BMI": bmi,
            "HvyAlcoholConsump": 1 if smoker == "Yes" else 0,
            "PhysHlth": phys_hlth,
            "MentHlth": ment_hlth,
            "PhysActivity": 1 if phys_active == "Yes" else 0,
            "DiffWalk": 1 if diff_walk == "Yes" else 0
        }
        
        # Convert to H2OFrame
        input_df = pd.DataFrame([input_dict])
        h2o_frame = h2o.H2OFrame(input_df)
        
        # Predict
        prediction = model.predict(h2o_frame)
        pred_df = prediction.as_data_frame()
        
        # Display results
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Prediction Results</div>', unsafe_allow_html=True)
        
        # Get risk probability
        risk = pred_df["p1"][0] * 100
        
        # Determine risk level and display appropriate message
        if risk > 70:
            risk_status = "high"
            risk_message = f"<div class='status-high'><strong>High Risk of Diabetes</strong><br>Your results indicate a high risk ({risk:.1f}%) for developing Type 2 Diabetes.</div>"
            clinical_rec = "<strong>Clinical recommendation:</strong> Urgent consultation with a healthcare provider is suggested."
        elif risk > 30:
            risk_status = "medium"
            risk_message = f"<div class='status-medium'><strong>Moderate Risk of Diabetes</strong><br>Your results indicate a moderate risk ({risk:.1f}%) for developing Type 2 Diabetes.</div>"
            clinical_rec = "<strong>Clinical recommendation:</strong> Preventive screening and lifestyle modifications advised."
        else:
            risk_status = "low"
            risk_message = f"<div class='status-low'><strong>Low Risk of Diabetes</strong><br>Your results indicate a low risk ({risk:.1f}%) for developing Type 2 Diabetes.</div>"
            clinical_rec = "<strong>Clinical recommendation:</strong> Maintain current health regimen and continue regular check-ups."
        
        st.markdown(risk_message, unsafe_allow_html=True)
        
        # Risk meter
        st.markdown('<div class="risk-meter">', unsafe_allow_html=True)
        st.progress(int(risk))
        st.markdown('<div class="risk-labels"><span class="risk-low">Low Risk</span><span class="risk-medium">Moderate Risk</span><span class="risk-high">High Risk</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Interpretation and recommendations
        st.markdown("### Analysis and Recommendations")
        st.markdown(clinical_rec, unsafe_allow_html=True)
        
        if risk > 30:
            st.markdown("""
            #### Key Risk Factors:
            - **BMI over 25** - Being overweight increases insulin resistance
            - **Physical inactivity** - Regular exercise helps control glucose levels
            - **High blood pressure** - Often co-occurs with Type 2 Diabetes
            - **High cholesterol** - Increases cardiovascular risk in diabetic patients
            
            #### Recommended Actions:
            1. Schedule a follow-up with your healthcare provider for blood glucose testing
            2. Consider consulting with a registered dietitian
            3. Aim for at least 150 minutes of moderate exercise weekly
            4. Monitor blood pressure and cholesterol regularly
            """)
        else:
            st.markdown("""
            #### Healthy Habits to Maintain:
            1. Regular physical activity (150+ minutes per week)
            2. Balanced diet rich in whole grains, lean proteins, and vegetables
            3. Maintain a healthy weight
            4. Continue regular health screenings
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Disclaimer
        st.info("**Disclaimer:** This assessment provides an estimate based on the information provided and should not replace professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment.")

# Shutdown H2O when app is closed
if st.session_state.h2o_initialized and not st.session_state.get('h2o_shutdown'):
    def shutdown_h2o():
        h2o.cluster().shutdown()
        st.session_state.h2o_shutdown = True
    
    # We can't directly call this on app close, but we can 
    # make it happen if the user refreshes or exits
    st.session_state.h2o_shutdown = False