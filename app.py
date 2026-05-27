import streamlit as st
import requests
import json

# --- PAGE CONFIGURATION (तुमचा जुना आवडता स्टाईलिश लूक) ---
st.set_page_config(page_title="Abhyas Kranti", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR BEAUTIFUL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        background-color: #4FFFB0;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3ddda0;
        color: black;
    }
    h1 { color: #1E3A8A; font-family: 'Helvetica Neue', sans-serif; }
    h3 { color: #0D9488; }
    </style>
""", unsafe_allow_html=True)

# --- AI CORE: DIRECT API CALL (FIXED FOR KEYERROR CANDIDATES) ---
def ask_gemini_ai(prompt_text):
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return "क्षमस्व, वैध API Key मिळालेला नाही. कृपया Streamlit Secrets तपासा."

    # गुगलचा थेट आणि सर्वात सुरक्षित v1beta एंडपॉइंट
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # गुगलच्या नवीन नियमांनुसार पेलोडची रचना
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are Abhyas Kranti AI Mentor. Answer the request thoroughly and clearly in Marathi language only, suitable for students. Request: {prompt_text}"
            }]
        }],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # --- सुरक्षित तपासणी (KeyError टाळण्यासाठी सुरक्षित रचना) ---
            if 'candidates' in response_data and response_data['candidates']:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text']
                elif 'finishReason' in candidate:
                    return f"माहिती ब्लॉक झाली आहे. कारण: {candidate['finishReason']}. कृपया पुन्हा प्रयत्न करा."
            
            return "गुगल सर्व्हरकडून रिकामे उत्तर आले आहे. कृपया पुन्हा प्रयत्न करा."
        else:
            return f"सर्व्हर एरर (Status Code: {response.status_code}). कृपया तुमची API Key किंवा इंटरनेट कनेक्शन तपासा."
            
    except Exception as e:
        return f"कनेक्शन एरर: {str(e)}"

# --- APP HEADER ---
st.title("🎓 Abhyas Kranti")
st.subheader("AI-Powered Educational Ecosystem for Rural India")
st.markdown("---")

# --- SIDEBAR: LOGIN & PROFILE ---
with st.sidebar:
    st.header("👤 User Profile")
    student_name = st.text_input("Student Name", placeholder="तुमचे नाव टाका")
    
    class_option = st.selectbox(
        "Select School/College Level",
        ["Primary School (Class 1-5)", "Middle School (Class 6-8)", "High School (Class 9-10)", "Junior College (Class 11-12)", "🎓 Higher Education / Degree"]
    )
    
    exam_target = st.selectbox(
        "Select Target Exam",
        ["NEET / JEE", "NDA / Defense", "MPSC / UPSC / Competitive", "Scholarship Exams (Class 5/8)", "School Board Exams"]
    )
    
    st.markdown("---")
    st.markdown("💡 *Abhyas Kranti AI Mentor नेहमी तुमच्यासोबत आहे!*")

# --- MAIN INTERFACE: NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🤖 AI Doubt Solver", "📅 Smart Study Planner", "🎓 Scholarship & Career Guide"])

# --- TAB 1: AI DOUBT SOLVER ---
with tab1:
    st.header("🤖 AI Doubt Solver")
    st.write("कोणताही प्रश्न विचारा आणि मिळवा सोपे मराठी उत्तर!")
    
    user_question = st.text_input("Enter your educational question here:", placeholder="उदा. प्रकाश संश्लेषण म्हणजे काय?")
    
    if st.button("Ask AI Mentor 🚀", key="ask_ai_btn"):
        if not student_name.strip():
            st.warning("⚠️ कृपया आधी डाव्या बाजूला तुमचे नाव टाका!")
        elif not user_question.strip():
            st.warning("⚠️ कृपया तुमचा प्रश्न टाईप करा.")
        else:
            with st.spinner("⏳ एआय उत्तर तयार करत आहे... कृपया वाट पाहा..."):
                full_prompt = f"Student Level: {class_option}. Exam Target: {exam_target}. Question: {user_question}"
                answer = ask_gemini_ai(full_prompt)
                st.markdown("### 📝 AI Mentor Response:")
                st.info(answer)

# --- TAB 2: SMART STUDY PLANNER ---
with tab2:
    st.header("📅 Smart Study Planner")
    st.write("तुमच्या उपलब्ध वेळेनुसार अभ्यासाचे वैयक्तिक वेळापत्रक बनवा.")
    
    study_hours = st.slider("तुम्ही दिवसातून किती तास अभ्यास करू शकता?", 1, 16, 6)
    
    if st.button("Generate My Study Plan 🗓️", key="planner_btn"):
        if not student_name.strip():
            st.warning("⚠️ कृपया आधी डाव्या बाजूला तुमचे नाव टाका!")
        else:
            with st.spinner("⏳ तुमचे वेळापत्रक बनवत आहे..."):
                planner_prompt = f"Create a beautiful daily study timetable for a {class_option} student targetting {exam_target} who can study {study_hours} hours a day. Write in clear Marathi with time blocks."
                plan_result = ask_gemini_ai(planner_prompt)
                st.markdown("### 🗓️ तुमचं वैयक्तिक वेळापत्रक:")
                st.success(plan_result)

# --- TAB 3: SCHOLARSHIP & CAREER GUIDE ---
with tab3:
    st.header("🎓 Scholarship & Career Guide")
    st.write("तुमच्यासाठी उपलब्ध असलेल्या सरकारी योजना आणि करिअरच्या संधी शोधा.")
    
    income_bracket = st.selectbox(
        "कुटुंबाचे वार्षिक उत्पन्न गट निवडा:",
        ["१ लाखापेक्षा कमी", "१ ते ३ lakh", "३ ते ८ लाख", "८ लाखांपेक्षा जास्त"]
    )
    
    if st.button("Find Scholarships & Schemes 🏛️", key="scholarship_btn"):
        if not student_name.strip():
            st.warning("⚠️ कृपया आधी डाव्या बाजूला तुमचे नाव टाका!")
        else:
            with st.spinner("⏳ माहिती शोधत आहे..."):
                scholarship_prompt = f"List best government scholarships and free education schemes in Maharashtra for a {class_option} student targetting {exam_target} with family income {income_bracket}. Provide response in Marathi text."
                scholarship_result = ask_gemini_ai(scholarship_prompt)
                st.markdown("### 🏛️ तुमच्यासाठी उपलब्ध योजना:")
                st.warning(scholarship_result)
