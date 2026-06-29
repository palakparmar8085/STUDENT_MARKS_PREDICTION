import streamlit as st
import joblib 
import pandas as pd

# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduPredict — Student Marks Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── LOAD MACHINE LEARNING MODEL ───────────────────────────────────────────────
@st.cache_resource
def load_prediction_model():
    try:
        return joblib.load("students_marks_predictor.joblib")
    except FileNotFoundError:
        return None

ml_model = load_prediction_model()

# ── CUSTOM CSS CUSTOMIZATION ──────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background: white;            
    }
    .stAppHeader {
        background-color: #2563EB;
        border-bottom: 2px solid #1D4ED8;
    }
    .stAppHeader::before {
        content: "🎓 Student Marks Prediction";
        font-weight: bold;
        font-size: 20px;
        position: absolute;
        left: 20px;
       font-family: "Source Sans Pro", sans-serif;
    }
    .big-container {
        background-color: #2563EB;
        border-radius: 0px;
        text-align: center;
        padding: 120px 30px;
        width: 100%;
        margin-bottom: 50px;
    }
    .big-title {
        font-size: 32px;
        margin-bottom: 6px;
    }
    .big-subtitle {
        font-size: 17px;
        opacity: 0.95;
    }
    .s-btn {
        margin-top: 35px;
        background-color: green;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 35px;
        border-radius: 50px;
        border: none;
        text-decoration: none;
        display: inline-block;
    }
    .s-btn:hover {
        background-color: #2EB774;
    }
    [data-testid="stForm"] {
        background-color: #2563EB;
        box-shadow: 0px 20px 50px rgba(0, 0, 0, 0.45);
        border-radius: 20px;
        padding: 60px 40px;
        border: 2px solid white;
        margin: 50px auto;
        max-width: 750px;
    }
    [data-testid="stForm"] label p {
        color: white;
        font-size: 16px;
        font-weight: bold;
    }
    [data-testid="stForm"] .stButton {
        text-align: center;
    }
    [data-testid="stTextInput"] [data-testid="InputInstructions"]{
        display:none;    
    }
    .visible-text-heading {
        color: #111827;
        font-size: 28px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .visible-text-p {
        color: #374151;
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    </style>
    
    <div class="big-container">
        <div class="big-title">🎓 Welcome to the Student Marks Prediction System</div>
        <div class="big-subtitle">Predict your performance based on key study indicators without login.</div>
        <a href="#prediction-section"><button class="s-btn">🎉 Get Started</button></a>
    </div>
    """, 
    unsafe_allow_html=True
)

# ── MARKETING & INFO SECTIONS ─────────────────────────────────────────────────
st.markdown("<p class='visible-text-heading'>Can you predict your exam marks before the result comes out?</p>", unsafe_allow_html=True)
st.markdown(
    "<p class='visible-text-p'>Yes, you can. Our marks predictor calculator estimates your final score before your result is officially out. "
    "Many students go through weeks of stress after an exam, unsure of what to expect. This anxiety distracts them from "
    "their studies and future plans. They are constantly stressed. An estimated score helps them move forward confidently "
    "and plan their next steps.</p>", 
    unsafe_allow_html=True
)
st.markdown("<p class='visible-text-p'>We help students like you with our marks predictor tool. It mathematically estimates your exam score based on your daily study hours.</p>", unsafe_allow_html=True)

st.markdown("<p class='visible-text-heading'>How to Use the Marks Predictor Calculator</p>", unsafe_allow_html=True)
st.markdown("<p class='visible-text-p'>Follow these simple steps to instantly evaluate and estimate the expected exam performance:</p>", unsafe_allow_html=True)
st.markdown("""
<div class='visible-text-p' style='margin-left: 20px;'>
1. <b>Enter Student Name:</b> Input the full name of the student in the designated text field.<br>
2. <b>Provide Study Hours:</b> Enter the average number of daily study hours dedicated to preparation.<br>
3. <b>Generate Prediction:</b> Click on the 'Predict' button to let the machine learning model calculate and display the estimated exam score based on the inputs provided.
</div>
""", unsafe_allow_html=True)

# Jump Link Anchor
st.markdown('<div id="prediction-section"></div>', unsafe_allow_html=True)

# ── PREDICTION FORM INTERFACE ─────────────────────────────────────────────────
with st.form(key="student_prediction_form"):
    st.markdown("<h1 style='text-align: center; color: white; font-size: 32px; margin-bottom: 25px;'>🎓 Predict Your Exam Marks</h1>", unsafe_allow_html=True)
    name = st.text_input("Enter Your Name", placeholder="Enter Full Name")
    study_hours_input = st.text_input("Enter Study Hours", placeholder="Enter a number between 1 and 10")
    button = st.form_submit_button("Predict Marks")

# ── PREDICTION LOGIC & VALIDATION ─────────────────────────────────────────────
if button:
    if ml_model is None:
        st.error("Model file 'students_marks_predictor.pkl' not found in this folder!")
    elif not name:
        st.error("Please enter your name.")
    elif not study_hours_input:
        st.error("Please enter study hours.")
    else:
        try:
            study_hours_num = int(study_hours_input)
            if 1 <= study_hours_num <= 10:
                input_df = pd.DataFrame([[study_hours_num]], columns=["study_hours"])
                prediction = ml_model.predict(input_df)
                predicted_marks = round(float(prediction[0][0]), 2)
                
                # Handling boundary condition for marks percentage
                if predicted_marks > 100:
                    predicted_marks = 100.0
                    
                output_html = f"<div style='background-color:#111827; color:#34d399; padding:16px; border-radius:10px; font-size:18px; font-weight:bold; border-left:5px solid #10b981; margin-top:20px;'>🎉 Congratulations {name}! Your predicted score is {predicted_marks}% based on {study_hours_num} hours of daily study.</div>"
                st.markdown(output_html, unsafe_allow_html=True)
            else:
                st.error("Please enter hours between 1 and 10.")
        except ValueError:
            st.error("Please enter a valid number for study hours.")