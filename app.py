import streamlit as st
import pandas as pd
import google.generativeai as genai
import sqlite3

# --- CONSTANTS & CONFIGURATION ---
st.set_page_config(
    page_title="Abhyas Kranti NEW - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM GLASSMORPHISM THEME (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #FFD700;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- LOCAL DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('abhyas_kranti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (name TEXT, mobile TEXT, exam TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- AI CORE: GOOGLE OFFICIAL SDK INTEGRATION ---
def ask_gemini_ai(prompt_text):
    # 🔴 महत्त्वाचा बदल: तुमच्या Google AI Studio चा मूळ की खालील अवतरण चिन्हात टाका!
    api_key = "AIzaSyAaLvSlQNWnEIljMlBzSve37SKM97SWLZw"
    
    if api_key == "YOUR_FREE_GEMINI_API_KEY_HERE" and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        
    if api_key == "YOUR_FREE_GEMINI_API_KEY_HERE" or not api_key:
        return "क्षमस्व, एआय सिस्टीम जोडण्यासाठी वैध API Key मिळालेला नाही."

    try:
        # अधिकृत गुगल एसडीके कॉन्फिगरेशन
        genai.configure(api_key=api_key)
        
        system_instruction = "You are Abhyas Kranti AI Mentor. Explain topics simply using local analogies, suitable for rural Indian students. Use Marathi language predominantly or simple English."
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"गुगल एआय कडून प्रतिसाद मिळाला नाही. त्रुटी: {str(e)}"

# --- APPLICATION FLOW / SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- APP HEADER ---
st.markdown("<h1 style='text-align: center;'>🚀 Abhyas Kranti NEW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>AI-Powered Educational Ecosystem for Rural India</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 1. USER REGISTRATION / LOGIN ---
if not st.session_state.logged_in:
    st.subheader("📝 विद्यार्थी नोंदणी / Student Registration")
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("विद्यार्थ्याचे पूर्ण नाव (Full Name):")
        student_mobile = st.text_input("मोबाईल नंबर (WhatsApp Number):", max_chars=10)
    with col2:
        target_exam = st.selectbox("तुम्ही कोणत्या परीक्षेची तयारी करत आहात?", 
                                   ["MPSC / UPSC", "NEET / JEE", "NDA / Defence", "स्कॉलरशिप परीक्षा (Class 5/8)", "इतर स्पर्धा परीक्षा"])
    
    if st.button("ॲप सुरू करा (Enter Ecosystem)"):
        if student_name and len(student_mobile) == 10:
            conn = sqlite3.connect('abhyas_kranti.db')
            c = conn.cursor()
            c.execute("INSERT INTO students VALUES (?, ?, ?)", (student_name, student_mobile, target_exam))
            conn.commit()
            conn.close()
            
            st.session_state.logged_in = True
            st.session_state.username = student_name
            st.session_state.exam = target_exam
            st.rerun()
        else:
            st.error("कृपया तुमचे नाव आणि वैध १० अंकी मोबाईल नंबर टाका.")

# --- MAIN LIVE DASHBOARD ---
else:
    st.sidebar.markdown(f"### 👤 स्वागत आहे, {st.session_state.username}!")
    st.sidebar.markdown(f"🎯 **लक्ष्य:** {st.session_state.exam}")
    if st.sidebar.button("लॉग आउट (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    # MULTI-TAB FEATURES INDEX
    menu = ["🤖 AI Doubt Solver", "📅 Smart Study Planner", "🎓 Scholarship & Careers"]
    choice = st.tabs(menu)

    # TAB 1: REAL WORKING AI MENTOR
    with choice[0]:
        st.markdown("<div class='card'><h3>🤖 एआय डाऊट सॉल्व्हर (Ask Any Question)</h3>", unsafe_allow_html=True)
        st.write("विज्ञान, गणित किंवा सामान्य ज्ञानाचा कोणताही प्रश्न विचारा, एआय तुम्हाला सोप्या भाषेत समजून सांगेल.")
        
        user_query = st.text_input("तुमचा प्रश्न इथे टाईप करा (उदा. प्रकाश संश्लेषण म्हणजे काय? / Newton's Laws):")
        
        if st.button("उत्तर शोधा (Ask AI)"):
            if user_query:
                with st.spinner("अभ्यास क्रांती एआय विचार करत आहे..."):
                    ai_response = ask_gemini_ai(user_query)
                    st.markdown("#### 📝 उत्तर / Response:")
                    st.write(ai_response)
            else:
                st.warning("कृपया आधी तुमचा प्रश्न टाईप करा.")
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: SMART STUDY PLANNER
    with choice[1]:
        st.markdown("<div class='card'><h3>📅 स्मार्ट STUDY प्लॅनर (AI Timetable)</h3>", unsafe_allow_html=True)
        daily_hours = st.slider("तुम्ही रोज किती तास अभ्यास करू शकता?", 1, 12, 4)
        
        if st.button("माझा अभ्यासाचा प्लॅन तयार करा"):
            with st.spinner("तुमचे वेळापत्रक तयार होत आहे..."):
                planner_prompt = f"Create a practical dynamic study timetable for a student preparing for {st.session_state.exam} who can study {daily_hours} hours a day. Give specific breakdown of subjects and breaks in Marathi language."
                ai_plan = ask_gemini_ai(planner_prompt)
                st.markdown("#### 📋 तुमच्यासाठी बनवलेले वेळापत्रक:")
                st.write(ai_plan)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: SCHOLARSHIP AND CAREERS
    with choice[2]:
        st.markdown("<div class='card'><h3>🎓 शिष्यवृत्ती आणि करिअर मार्गदर्शन</h3>", unsafe_allow_html=True)
        income_bracket = st.selectbox("तुमच्या कुटुंबाचे वार्षिक उत्पन्न निवडा:", 
                                      ["१ लाखापेक्षा कमी", "१ ते ३ लाख", "३ ते ८ लाख", "८ लाखांपेक्षा जास्त"])
        
        if st.button("योग्य योजना शोधा"):
            with st.spinner("शोधत आहे..."):
                scholarship_prompt = f"List the top 3 central or state government scholarships available for a student in Maharashtra with an annual family income of {income_bracket} preparing for {st.session_state.exam}. Explain in Marathi."
                scholarship_data = ask_gemini_ai(scholarship_prompt)
                st.markdown("#### 🌟 तुमच्यासाठी उपलब्ध असणाऱ्या योजना:")
                st.write(scholarship_data)
        st.markdown("</div>", unsafe_allow_html=True)
