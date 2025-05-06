import streamlit as st
import pandas as pd
import pickle
import os


# Load the model
def load_model():
    try:
        with open('gpu_automl_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the prediction function
def load_predict_function():
    try:
        with open('predict_function.pkl', 'rb') as predict_file:
            return pickle.load(predict_file)
    except Exception as e:
        st.error(f"Error loading prediction function: {e}")
        return None

# Predict function using pandas instead of cuDF
def predict_cardiovascular_risk(bmi, age, high_chol, high_bp):
    try:
        data = pd.DataFrame({
            'high_bp': [high_bp],
            'age': [age],
            'high_chol': [high_chol],
            'BMI': [bmi]
        })

        model = load_model()
        if model is None:
            return None, None
        
        prediction = model.predict(data)
        prediction_proba = model.predict_proba(data) if hasattr(model, 'predict_proba') else None
        
        return int(prediction[0]), prediction_proba[0][1] if prediction_proba is not None else None
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None, None

# App UI
st.set_page_config(
    page_title="HealthGuard AI - Cardio Risk Predictor", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: #1e1e1e;
    }
    
    /* Header styling */
    .title-font {
        font-size: 2.8rem;
        font-weight: 700;
        color: #3498db;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .subtitle-font {
        font-size: 1.2rem;
        color: #f0f0f0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card container styling */
    .card {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    /* Form styling */
    .form-header {
        color: #3498db;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Results styling */
    .results-container {
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .high-risk {
        background-color: rgba(239, 68, 68, 0.2);
        border-left: 4px solid #ef4444;
    }
    
    .low-risk {
        background-color: rgba(34, 197, 94, 0.2);
        border-left: 4px solid #22c55e;
    }
    
    .risk-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #f0f0f0;
    }
    
    .risk-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f0f0f0;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #2d2d2d;
        color: #f0f0f0;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #3d3d3d;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 2rem;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Page layout
with st.container():
    st.markdown('<h1 class="title-font">Cardiovascular Disease Risk Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-font">This interactive tool helps evaluate your risk of developing cardiovascular disease based on key health factors.</p>', unsafe_allow_html=True)

    # Create a three-column layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Input form in a card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">📝 Patient Information</div>', unsafe_allow_html=True)
        
        with st.form("patient_form"):
            # Create two columns for the form
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                age = st.slider(
                    "Age (Years)", 
                    30, 100, 50, 
                    help="The age of the patient in years"
                )
                
                bmi_desc = "Body Mass Index - a measure of body fat based on height and weight"
                st.markdown(f'<div>BMI <span class="tooltip">ℹ️<span class="tooltiptext">{bmi_desc}</span></span></div>', unsafe_allow_html=True)
                bmi = st.slider("", 15.0, 40.0, 25.0, step=0.1, key="bmi_slider")
                
            with form_col2:
                bp_desc = "High blood pressure is defined as systolic BP ≥ 130 mmHg or diastolic BP ≥ 80 mmHg"
                st.markdown(f'<div>High Blood Pressure <span class="tooltip">ℹ️<span class="tooltiptext">{bp_desc}</span></span></div>', unsafe_allow_html=True)
                high_bp = st.radio("", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", horizontal=True, key="bp_radio")
                
                chol_desc = "High cholesterol is defined as total cholesterol ≥ 200 mg/dL"
                st.markdown(f'<div>High Cholesterol <span class="tooltip">ℹ️<span class="tooltiptext">{chol_desc}</span></span></div>', unsafe_allow_html=True)
                high_chol = st.radio("", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", horizontal=True, key="chol_radio")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Assess Cardiovascular Risk")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction logic
        if submitted:
            model = load_model()
            
            if model is None:
                st.error("Could not load the prediction model. Please check the model files.")
            else:
                try:
                    # Show loading indicator
                    with st.spinner("Analyzing your risk factors..."):
                        # Simulate computation time
                        import time
                        time.sleep(1)
                        
                        # Perform Prediction
                        prediction, proba = predict_cardiovascular_risk(bmi, age, high_chol, high_bp)
                    
                    # Display risk factors summary
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="form-header">📊 Risk Factors Summary</div>', unsafe_allow_html=True)
                    
                    risk_cols = st.columns(4)
                    with risk_cols[0]:
                        st.metric("Age", f"{age} years")
                    with risk_cols[1]:
                        st.metric("BMI", f"{bmi:.1f}")
                    with risk_cols[2]:
                        st.metric("High Blood Pressure", "Yes" if high_bp else "No")
                    with risk_cols[3]:
                        st.metric("High Cholesterol", "Yes" if high_chol else "No")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display prediction result
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="form-header">🧑‍⚕️ Assessment Result</div>', unsafe_allow_html=True)
                    
                    if prediction == 1:
                        risk_class = "high-risk"
                        risk_icon = "⚠️"
                        risk_text = "High Risk of Cardiovascular Disease"
                    else:
                        risk_class = "low-risk"
                        risk_icon = "✅"
                        risk_text = "Low Risk of Cardiovascular Disease"
                    
                    st.markdown(f'''
                    <div class="results-container {risk_class}">
                        <div class="risk-title">{risk_icon} {risk_text}</div>
                        <div>Risk probability: <span class="risk-value">{proba:.1%}</span></div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Risk probability visualization
                    st.progress(float(proba))
                    
                    # Recommendations based on risk level
                    st.markdown("### Recommendations")
                    if prediction == 1:
                        st.markdown("""
                        - Consider consulting with a healthcare provider
                        - Regular monitoring of blood pressure and cholesterol
                        - Maintain a heart-healthy diet and regular exercise
                        - Consider medication if recommended by your doctor
                        """)
                    else:
                        st.markdown("""
                        - Continue maintaining a healthy lifestyle
                        - Regular check-ups with your healthcare provider
                        - Stay physically active and maintain a balanced diet
                        - Monitor your blood pressure and cholesterol periodically
                        """)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Developed with ❤️ using Streamlit and Machine Learning | Not for clinical use", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)