import streamlit as st
import requests
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Abhyas Kranti NEW", page_icon="🚀", layout="wide")

# --- AI CORE: DIRECT API CALL (NO LIBRARIES, NO VERSION ERRORS) ---
def ask_gemini_ai(prompt_text):
    # Streamlit Secrets मधून की मिळवणे
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    if not api_key:
        return "क्षमस्व, एआय सिस्टीम जोडण्यासाठी वैध API Key मिळालेला नाही. कृपया Streamlit Secrets तपासा."

    # गुगलचा थेट आणि सर्वात नवीन अधिकृत v1 एंडपॉइंट (यात कधीही ४०४ एरर येत नाही)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # सोप्या मराठी उत्तरांसाठी सिस्टीम इंस्ट्रक्शन थेट पेलोडमध्ये समाविष्ट
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are Abhyas Kranti AI Mentor. Explain topics simply using local analogies, suitable for school students in Marathi language only. Context: {prompt_text}"
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        # एआय कडून आलेले उत्तर वाचणे
        if response.status_code == 200:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = response_data.get('error', {}).get('message', 'Unknown Error')
            return f"त्रुटी (Status {response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"कनेक्शन होऊ शकले नाही. त्रुटी: {str(e)}"

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
        st.success(f"स्वागत आहे, {st.session_state.username}!")
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
        "तुमचा प्रश्न इथे टाईप करा (उदा. प्रकाश संश्लेषण म्हणजे काय?):",
        key="ai_question_input"
    )
    
    if st.button("उत्तर शोधा (Ask AI)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी डाव्या बाजूला तुमचे नाव टाकून लॉगिन करा!")
        elif not user_question.strip():
            st.warning("कृपया आधी तुमचा प्रश्न टाईप करा.")
        else:
            with st.spinner("एआय उत्तर तयार करत आहे... कृपया वाट पाहा..."):
                answer = ask_gemini_ai(user_question)
                st.markdown("### 📝 उत्तर / Response:")
                st.info(answer)

# --- TAB 2: SMART STUDY PLANNER ---
with tab2:
    st.header("📅 स्मार्ट अभ्यास नियोजक (Smart Planner)")
    available_hours = st.slider("तुम्ही दिवसातून किती तास अभ्यास करू शकता?", 1, 16, 6)
    
    if st.button("नियोजन तयार करा (Generate Plan)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी लॉगिन करा!")
        else:
            with st.spinner("वेळापत्रक बनवत आहे..."):
                planner_prompt = f"Create a daily study timetable for {st.session_state.exam_target} student with {available_hours} hours study time in Marathi."
                plan_result = ask_gemini_ai(planner_prompt)
                st.success(plan_result)

# --- TAB 3: SCHOLARSHIP & CAREERS ---
with tab3:
    st.header("🎓 शिष्यवृत्ती आणि करिअर मार्गदर्शन")
    family_income = st.selectbox("कुटुंबाचे वार्षिक उत्पन्न गट निवडा:", ["१ लाखापेक्षा कमी", "१ ते ३ लाख", "३ ते ८ लाख", "८ लाखांपेक्षा जास्त"])
    
    if st.button("योग्य योजना शोधा (Find Schemes)"):
        if not st.session_state.logged_in:
            st.warning("कृपया आधी लॉगिन करा!")
        else:
            with st.spinner("माहिती गोळा करत आहे..."):
                scholarship_prompt = f"List government scholarships in Maharashtra for {st.session_state.exam_target} student with family income {family_income} in Marathi."
                scholarship_result = ask_gemini_ai(scholarship_prompt)
                import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# v1beta व्हर्जन वापरून मॉडेल कॉल करणे
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"response_mime_type": "text/plain"}
)
                st.warning(scholarship_result)
