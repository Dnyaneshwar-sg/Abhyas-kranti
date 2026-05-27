import streamlit as st
import pandas as pd
import requests
import json
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

# --- LOCAL DATABASE SETUP (For Students Data) ---
def init_db():
    conn = sqlite3.connect('abhyas_kranti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (name TEXT, mobile TEXT, exam TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- AI CORE: GEMINI API INTEGRATION ---
def ask_gemini_ai(prompt_text):
    # 🔴 महत्त्वाचा बदल: खालील ओळीत तुमचा मूळ API Key डबल कोट्सच्या मध्ये पेस्ट करा!
    api_key = "YOUR_FREE_GEMINI_API_KEY_HERE"
    
    # जर वरील की बदलला नसेल तर बॅकअप म्हणून Streamlit Secrets तपासणे
    if api_key == "YOUR_FREE_GEMINI_API_KEY_HERE" and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        
    if api_key == "YOUR_FREE_GEMINI_API_KEY_HERE" or not api_key:
        return "क्षमस्व, एआय सिस्टीम जोडण्यासाठी API Key मिळालेला नाही. कृपया app.py मध्ये ओळ ५७ तपासा."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = "You are Abhyas Kranti AI Mentor. Explain topics simply using local analogies, suitable for rural Indian students. Use Marathi or simple English."
    
    data = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nQuestion: {prompt_text}"}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"गुगल एआय सर्व्हरने त्रुटी दिली (Status Code: {response.status_code}). कृपया तुमचा API Key वैध असल्याची खात्री करा."
    except Exception as e:
        return f"कनेक्शन त्रुटी आढळली: {str(e)}"

# --- AUTOMATION: MAKE.COM WEBHOOK FUNCTION ---
def send_to_make_webhook(name, mobile, exam):
    MAKE_WEBHOOK_URL = "https://hook.us1.make.com/your_actual_webhook_id_here"
    payload = {
        "student_name": name,
        "mobile_number": mobile,
        "target_exam": exam,
        "status": "Registered"
    }
    try:
        requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=5)
    except Exception:
        pass

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
            
            send_to_make_webhook(student_name, student_mobile, target_exam)
            
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
        st.markdown("<div class='card'><h3>📅 स्मार्ट स्टडी प्लॅनर (AI Timetable)</h3>", unsafe_allow_html=True)
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
                                      ["१ लाखापेक्षा कमी", "१ ते ३ लाख", "३ ते ८ lakh", "८ लाखांपेक्षा जास्त"])
        
        if st.button("योग्य योजना शोधा"):
            with st.spinner("शोधत आहे..."):
                scholarship_prompt = f"List the top 3 central or state government scholarships or financial aids available for a student in Maharashtra with an annual family income of {income_bracket} preparing for {st.session_state.exam}. Explain in Marathi."
                scholarship_data = ask_gemini_ai(scholarship_prompt)
                st.markdown("#### 🌟 तुमच्यासाठी उपलब्ध असणाऱ्या योजना:")
                st.write(scholarship_data)
        st.markdown("</div>", unsafe_allow_html=True)
