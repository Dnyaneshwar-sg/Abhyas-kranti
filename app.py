import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Abhyas Kranti NEW", page_icon="🚀", layout="wide")

# --- DATABASE / UTILS (DUMMY FOR SYSTEM INITIALIZATION) ---
def init_db():
    # डेटाबेसची रचना भविष्यातील वापरासाठी सुरक्षित ठेवली आहे
    pass

init_db()

# --- AI CORE: GOOGLE OFFICIAL SDK INTEGRATION (UPDATED FOR V1) ---
def ask_gemini_ai(prompt_text):
    # १. सर्वप्रथम Streamlit Secrets मधून की शोधणे
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    # २. जर सिक्रेट्समध्ये नसेल तर लोकल किंवा एन्व्हायर्नमेंट व्हेरिएबल तपासणे
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", None)
        
    # ३. तरीही की मिळाली नाही तर विद्यार्थ्याला एरर दाखवणे
    if not api_key or api_key == "YOUR_FREE_GEMINI_API_KEY_HERE":
        return "क्षमस्व, एआय सिस्टीम जोडण्यासाठी वैध API Key मिळालेला नाही. कृपया Streamlit Secrets तपासा."

    try:
        # गुगलच्या लेटेस्ट लायब्ररीनुसार कॉन्फिगरेशन
        genai.configure(api_key=api_key)
        
        # सिस्टीम इंस्ट्रक्शन (मराठीत सोप्या उत्तरांसाठी मार्गदर्शन)
        system_instruction = (
            "You are Abhyas Kranti AI Mentor. Explain topics simply using local analogies, "
            "suitable for school students in Marathi language only."
        )
        
        # नवीन v1 स्टँडर्डनुसार मॉडेल लोड करणे
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # उत्तर जनरेट करणे
        response = model.generate_content(prompt_text)
        return response.text
        
    except Exception as e:
        return f"गुगल एआय कडून प्रतिसाद मिळाला नाही. त्रुटी: {str(e)}"

# --- APP HEADER ---
st.title("🚀 Abhyas Kranti NEW")
st.subheader("AI-Powered Educational Ecosystem for Rural India")
st.markdown("---")

# --- LOGIN / SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.exam_target = "NEET / JEE"

# --- SIDEBAR LOGIN ---
with st.sidebar:
    st.header("👤 विद्यार्थी लॉगिन (Login)")
    if not st.session_state.logged_in:
        name = st.text_input("विद्यार्थ्याचे नाव (Student Name):")
        target = st.selectbox("लक्ष्य परीक्षा (Target Exam):", ["NEET / JEE", "MPSC / UPSC", "Scholarship (Class 5/8)", "NDA / Defense"])
        if st.button("लॉगिन करा (Login)"):
            if name.strip():
                st.session_state.logged_in = True
                st.session_state.username = name
                st.session_state.exam_target = target
                st.rerun()
            else:
                st.warning("कृपया नाव टाईप करा.")
    else:
        st.success(f"swagat aahe, {st.session_state.username}!")
        st.info(f"🎯 लक्ष्य: {st.session_state.exam_target}")
        if st.button("लॉग आऊट (Logout)"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🤖 AI Doubt Solver", "📅 Smart Study Planner", "🎓 Scholarship & Careers"])

# --- TAB 1: AI DOUBT SOLVER ---
with tab1:
    st.header("😊 एआय डाऊट सॉल्व्हर (Ask Any Question)")
    st.write("विज्ञान, गणित किंवा सामान्य ज्ञानाचा कोणताही प्रश्न विचारा, एआय तुम्हाला सोप्या भाषेत समजून सांगेल.")
    
    user_question = st.text_input(
        "तुमचा प्रश्न इथे टाईप करा (उदा. प्रकाश संश्लेषण म्हणजे काय? / Newton's Laws):",
        key="ai_question_input"
    )
    
    if st.button("उत्तर शोधा (Ask AI)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी डाव्या बाजूला तुमचे नाव टाकून लॉगिन करा!")
        elif not user_question.strip():
            st.warning("कृपया आधी तुमचा प्रश्न टाईph करा.")
        else:
            with st.spinner("एआय उत्तर तयार करत आहे... कृपया वाट पाहा..."):
                # मुख्य परीक्षा ध्येयाचा संदर्भ प्रश्नाला जोडणे
                full_prompt = f"Student Target: {st.session_state.exam_target}. Question: {user_question}"
                answer = ask_gemini_ai(full_prompt)
                
                st.markdown("### 📝 उत्तर / Response:")
                st.info(answer)

# --- TAB 2: SMART STUDY PLANNER ---
with tab2:
    st.header("📅 स्मार्ट अभ्यास नियोजक (Smart Planner)")
    st.write("तुमच्या उपलब्ध वेळेनुसार अभ्यासाचे अचूक वेळापत्रक तयार करा.")
    
    available_hours = st.slider("तुम्ही दिवसातून किती तास अभ्यास करू शकता?", 1, 16, 6)
    
    if st.button("नियोजन तयार करा (Generate Plan)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी लॉगिन करा!")
        else:
            with st.spinner("तुमचे वेळापत्रक बनवत आहे..."):
                planner_prompt = f"Create a detailed self-study daily timetable for a student preparing for {st.session_state.exam_target} who can study {available_hours} hours a day. Provide response in Marathi with clear time blocks."
                plan_result = ask_gemini_ai(planner_prompt)
                st.markdown("### 🗓️ तुमचे वेळापत्रक:")
                st.success(plan_result)

# --- TAB 3: SCHOLARSHIP & CAREERS ---
with tab3:
    st.header("🎓 शिष्यवृत्ती आणि करिअर मार्गदर्शन")
    st.write("तुमच्या शैक्षणिक उद्दिष्टांनुसार योग्य सरकारी योजना आणि शिष्यवृत्ती शोधा.")
    
    family_income = st.selectbox("कुटुंबाचे वार्षिक उत्पन्न गट निवडा:", ["१ लाखापेक्षा कमी", "१ ते ३ लाख", "३ ते ८ लाख", "८ लाखांपेक्षा जास्त"])
    
    if st.button("योग्य योजना शोधा (Find Schemes)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी लॉगिन करा!")
        else:
            with st.spinner("माहिती गोळा करत आहे..."):
                scholarship_prompt = f"List government scholarships, financial aid, and career paths available in Maharashtra/India for a student targetting {st.session_state.exam_target} with family income category {family_income}. Provide the output in Marathi text."
                scholarship_result = ask_gemini_ai(scholarship_prompt)
                st.markdown("### 🏛️ तुमच्यासाठी उपलब्ध संधी:")
                st.warning(scholarship_result)
