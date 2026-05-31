import streamlit as st
from supabase import create_client, Client
import pandas as pd
import requests
import json

# --- १. Secrets मधून सुपाबेसच्या चाव्या लोड करणे ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("कृपया Streamlit Secrets मध्ये SUPABASE_URL आणि SUPABASE_KEY SET करा.")

# --- २. पेज कॉन्फिगरेशन ---
st.set_page_config(
    page_title="Abhyas Kranti Ultimate Portal - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ३. ग्लोबल भाषा आणि राज्य मॅपिंग ---
languages_map = {
    "मराठी (Marathi) - महाराष्ट्र": "Marathi",
    "English - Pan India": "English",
    "हिंदी (Hindi) - उत्तर प्रदेश / बिहार / दिल्ली": "Hindi",
    "Gujarati (ગુજરાતી) - ગુજરાત": "Gujarati",
    "Kannada (ಕನ್ನಡ) - ಕರ್ನಾಟಕ": "Kannada",
    "Tamil (தமிழ்) - தமிழ்நாடு": "Tamil",
    "Telugu (తెలుగు) - ఆంధ్రప్రదేశ్ / తెలంగాణ": "Telugu",
    "Punjabi (ਪੰਜਾਬੀ) - ਪੰਜਾਬ": "Punjabi",
    "Bengali (বাংলা) - পশ্চিমবঙ্গ": "Bengali"
}

# --- ४. महा-डायनॅमिक इंटरफेस ट्रान्सलेशन मॅट्रिक्स ---
UI_LANG_MATRIX = {
    "Marathi": {
        "menu_lbl": "🌍 भाषा व राज्य निवडा (Select Language):",
        "dash_menu": "🏠 मुख्य पान (Dashboard)",
        "sandbox_menu": "⚡ ६-इन-१ AI सँडबॉक्स",
        "doubt_menu": "🧠 शंका निरसन केंद्र",
        "login_menu": "🔐 लॉगिन / प्रोफाईल",
        "tabs": ["🧠 २४/७ शंका निरसन शिक्षक", "📅 अभ्यास वेळापत्रक", "🛡️ स्कॉलरशिप इंजिन", "🎯 स्मार्ट मॉक टेस्ट", "🏢 करिअर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "तुमचा शैक्षणिक किंवा स्पर्धा परीक्षेचा कठीण प्रश्न इथे टाईप करा:",
        "btn1_lbl": "🚀 शंका निरसन करा (Instant Solution)",
        "q2_lbl": "कोणत्या परीक्षेची तयारी करत आहात? (उदा. NEET, JEE, MPSC, ६ वी स्कॉलरशिप)",
        "s2_lbl": "रोज अभ्यासासाठी किती तास उपलब्ध आहेत?",
        "btn2_lbl": "🚀 स्मार्ट वेळापत्रक तयार करा",
        "sel3_lbl": "विद्यार्थ्याची शैक्षणिक पातळी / इयत्ता निवडा:",
        "edu_opts": ["इयत्ता १ ली ते ४ थी", "इयत्ता ५ वी ते ७ वी", "इयत्ता ८ वी ते १० वी (SSC)", "इयत्ता ११ वी आणि १२ वी (HSC/NEET/JEE)", "पदवी शिक्षण (Undergraduate)"],
        "inc3_lbl": "कौटुंबिक वार्षिक उत्पन्न निवडा:",
        "inc_opts": ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाख ते ₹८ लाख"],
        "cat3_lbl": "प्रवर्ग / जात / आरक्षित श्रेणी (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 पात्र स्कॉलरशिप शोधा",
        "sel4_lbl": "मॉक टेस्टसाठी विषय निवडा:",
        "exam_tiers": ["भौतिकशास्त्र (Physics)", "रसायनशास्त्र (Chemistry)", "जीवशास्त्र (Biology)", "गणित (Mathematics)", "सामान्य ज्ञान (GK)"],
        "txt4_lbl": "तुम्ही निवडलेल्या विषयाचा कोणताही सराव प्रश्न किंवा टॉपिक लिहा (उदा. Optics, Thermodynamics):",
        "btn4_lbl": "🚀 AI मॉक टेस्ट प्रश्न आणि उत्तर विश्लेषण मिळवा",
        "sel5_lbl": "विद्याशाखा / प्रवाह निवडा:",
        "streams": ["कला शाखा (Arts)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तांत्रिक व मेडिकल"],
        "rad5_lbl": "करिअरची व्याप्ती (Scope):",
        "scopes": ["स्थानिक आणि राष्ट्रीय संधी", "जागतिक संधी (Global & International)"],
        "txt5_lbl": "विद्यार्थ्याची वैयक्तिक आवड (उदा. सोलर बिझनेस, डेटा सायन्स):",
        "btn5_lbl": "🚀 करिअर रोडमॅप व लिंक्स मिळवा"
    },
    "English": {
        "menu_lbl": "🌍 Select Language & State:",
        "dash_menu": "🏠 Main Dashboard",
        "sandbox_menu": "⚡ 6-in-1 AI Sandbox",
        "doubt_menu": "🧠 Doubt Solver",
        "login_menu": "🔐 Login / Profile",
        "tabs": ["🧠 24/7 AI Doubt Solver", "📅 Study Planner", "🛡️ Scholarship Engine", "🎯 Smart Mock Test", "🏢 Career Guide", "🌐 Language Hub"],
        "q1_lbl": "Type your academic or exam doubt here:",
        "btn1_lbl": "🚀 Solve My Doubt Instantly",
        "q2_lbl": "Which exam are you preparing for? (NEET, JEE, UPSC, etc.)",
        "s2_lbl": "How many hours can you study daily?",
        "btn2_lbl": "🚀 Create Smart Schedule",
        "sel3_lbl": "Select Educational Level / Grade:",
        "edu_opts": ["1st - 4th Grade", "5th - 7th Grade", "8th - 10th Grade (SSC)", "11th & 12th Grade (HSC)", "Undergraduate"],
        "inc3_lbl": "Select Annual Family Income:",
        "inc_opts": ["Below ₹1.5 Lakhs", "₹1.5 Lakhs to ₹3 Lakhs", "₹3 Lakhs to ₹8 Lakhs"],
        "cat3_lbl": "Type Category / Reservation (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 Find Eligible Scholarships",
        "sel4_lbl": "Select Subject for Mock Test:",
        "exam_tiers": ["Physics", "Chemistry", "Biology", "Mathematics", "General Knowledge"],
        "txt4_lbl": "Enter specific topic for Mock Question (e.g., Optics, Thermodynamics):",
        "btn4_lbl": "🚀 Generate AI Mock Question & Evaluation",
        "sel5_lbl": "Select Academic Stream:",
        "streams": ["Arts & Humanities", "Commerce & Management", "Pure & Applied Sciences", "Technical & Medical"],
        "rad5_lbl": "Career Scope Level:",
        "scopes": ["Local & National Opportunities", "Global Opportunities"],
        "txt5_lbl": "Your Core Area of Interest (e.g., Solar, Data Science):",
        "btn5_lbl": "🚀 Generate Career Roadmap & Links"
    }
}

# --- ५. प्रगत हाय-कॉन्ट्रास्ट विजिबिलिटी स्टायलिंग (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; }
    
    .stApp { background: #0d1117; color: #f0f6fc !important; }
    
    /* इनपुट बॉक्सेस मधील अक्षरे पांढरी व स्पष्ट दिसण्यासाठी CSS */
    input[type="text"], .stTextInput input, .stSelectbox div[data-baseweb="select"], textarea {
        color: #ffffff !important;
        background-color: #1f242c !important;
        border: 2px solid #444c56 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    /* इनपुट फिल्डच्या वरच्या लेबल्सचा रंग पांढरा करणे */
    div[data-testid="stWidgetLabel"] p, label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
    }
    
    /* ड्रॉपडाऊनच्या आत उघडणारे पर्याय पांढरे करणे */
    div[data-baseweb="popover"] li {
        color: #ffffff !important;
        background-color: #1f242c !important;
    }

    /* डाव्या बाजूचा प्रीमियम विजिबिलिटी साईडबार */
    [data-testid="stSidebar"] {
        background-color: #070a0e !important; 
        border-right: 3px solid #FFD700 !important;
    }
    
    /* मुख्य शिर्षक डिझाईन */
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem; display: block;
        margin-bottom: 5px;
    }
    
    /* टॅब सुशोभीकरण */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] {
        height: 52px; background-color: #21262d; border-radius: 8px;
        color: #ffffff !important; font-weight: 700 !important; font-size: 1.15rem !important;
    }
    .stTabs [aria-selected="true"] { background-color: #FFD700 !important; color: #0d1117 !important; }
    
    .glass-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .footer-container { border-top: 1px solid #30363d; padding-top: 25px; margin-top: 60px; text-align: center; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

# --- ६. पहिली सुरक्षित भाषा निवड लोड करणे ---
if "global_language_selector" in st.session_state:
    selected_lang_key = st.session_state["global_language_selector"]
else:
    selected_lang_key = "मराठी (Marathi) - महाराष्ट्र"

target_lang = languages_map.get(selected_lang_key, "Marathi")
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX.get("English", UI_LANG_MATRIX["Marathi"]))

# --- ७. डाव्या बाजूचा साईडबार ---
selected_display_lang = st.sidebar.selectbox(
    "🌍 भाषा निवडा / Select Language:",
    list(languages_map.keys()),
    index=list(languages_map.keys()).index(selected_lang_key) if selected_lang_key in languages_map else 0,
    key="global_language_selector"
)

target_lang = languages_map[selected_display_lang]
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX.get("English", UI_LANG_MATRIX["Marathi"]))

# --- स्थिर कीज (Static Keys) वर आधारित सुरक्षित नॅव्हिगेशन बार ---
modes_keys = ["dash", "sandbox", "doubt", "login"]
mode_display = {
    "dash": current_ui["dash_menu"],
    "sandbox": current_ui["sandbox_menu"],
    "doubt": current_ui["doubt_menu"],
    "login": current_ui["login_menu"]
}

if "current_app_mode_key" not in st.session_state:
    st.session_state["current_app_mode_key"] = "dash"

nav_cols = st.columns(4)
for i, key in enumerate(modes_keys):
    with nav_cols[i]:
        is_active = (st.session_state["current_app_mode_key"] == key)
        if st.button(mode_display[key], key=f"nav_btn_{key}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state["current_app_mode_key"] = key
            st.rerun()

app_mode = st.session_state["current_app_mode_key"]
st.markdown("---")

# --- ८. AI कॉल फंक्शन (Groq API) ---
def fetch_ai_response(prompt_text, system_setting):
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": system_setting}, {"role": "user", "content": prompt_text}],
            "temperature": 0.4, "max_tokens": 1500
        }
        response = requests.post(groq_url, headers=headers, data=json.dumps(payload))
        return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"Error: {response.status_code}"
    except Exception as e: return f"Error: {e}"

base_ai_instruction = f"You are 'Abhyas Kranti' AI Engine. Respond ONLY in {target_lang}. Keep explanations highly academic, clear, encouraging, and tailored for rural/struggling students."

# ==========================================
# विभाग १: Dashboard
# ==========================================
if app_mode == "dash":
    st.markdown('<span class="main-title">Abhyas Kranti National Portal</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown(f"**🌍 Active Language Context:** `{selected_display_lang}`")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card"><h3>🎯 २४/७ मोफत मार्गदर्शन</h3><p style="color:#c9d1d9;">महागड्या क्लासेसची फी न परवडणाऱ्या विद्यार्थ्यांसाठी एक पूर्णपणे मोफत, हाय-स्पीड आणि थेट मातृभाषेत शिकवणारी प्रणाली.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><h3>🚀 ८०% यशाचा फॉर्म्युला</h3><p style="color:#c9d1d9;">मॉक टेस्ट आणि इन्स्टंट शंका निरसन यांच्या थेट मिलाफामुळे ग्रामीण भागातील मुले पहिल्याच प्रयत्नात परीक्षा उत्तीर्ण होऊ शकतील.</p></div>', unsafe_allow_html=True)

# ==========================================
# विभाग २: ६-इन-१ AI सँडबॉक्स (मुख्य इंजिन)
# ==========================================
elif app_mode == "sandbox":
    st.markdown(f'<span class="main-title">{current_ui["sandbox_menu"]}</span>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(current_ui["tabs"])

    # २४/७ शंका निरसन शिक्षक
    with tab1:
        st.markdown(f"### {current_ui['tabs'][0]}")
        user_query = st.text_area(current_ui["q1_lbl"], key="q1_sandbox", height=100)
        if st.button(current_ui["btn1_lbl"], key="btn1_sandbox"):
            with st.spinner("AI शिक्षक उत्तर तयार करत आहेत..."):
                ans = fetch_ai_response(user_query, base_ai_instruction + " Act as a world-class teacher. Break down the concept into step-by-step easy formulas.")
                st.markdown(f'<div class="glass-card" style="border-left: 5px solid #FFD700;">{ans}</div>', unsafe_allow_html=True)

    # अभ्यास वेळापत्रक
    with tab2:
        st.markdown(f"### {current_ui['tabs'][1]}")
        exam_target = st.text_input(current_ui["q2_lbl"], "NEET Exam", key="q2")
        hours = st.slider(current_ui["s2_lbl"], 1, 12, 6, key="s2")
        if st.button(current_ui["btn2_lbl"], key="btn2"):
            with st.spinner("नियोजन तयार होत आहे..."):
                st.write(fetch_ai_response(f"Exam: {exam_target}, Hours available daily: {hours}", base_ai_instruction + " Create a practical daily timeline and weekly goals."))

    # स्कॉलरशिप इंजिन
    with tab3:
        st.markdown(f"### {current_ui['tabs'][2]}")
        edu = st.selectbox(current_ui["sel3_lbl"], current_ui["edu_opts"], key="edu_lvl")
        inc = st.selectbox(current_ui["inc3_lbl"], current_ui["inc_opts"], key="inc_lvl")
        cat = st.text_input(current_ui["cat3_lbl"], "OBC / Open", key="cat")
        if st.button(current_ui["btn3_lbl"], key="btn3"):
            with st.spinner("स्कॉलरशिप शोधत आहे..."):
                st.write(fetch_ai_response(f"Education: {edu}, Income Tier: {inc}, Category: {cat}", base_ai_instruction + " Suggest elite Government and Corporate Scholarships with criteria."))

    # स्मार्ट मॉक टेस्ट (सुधारित)
    with tab4:
        st.markdown(f"### {current_ui['tabs'][3]}")
        subject_selected = st.selectbox(current_ui["sel4_lbl"], current_ui["exam_tiers"], key="ex_lvl")
        topic_selected = st.text_input(current_ui["txt4_lbl"], "Newton's Laws of Motion", key="ex_name")
        
        if st.button(current_ui["btn4_lbl"], key="btn4"):
            with st.spinner("AI मॉक प्रश्न आणि त्याचे सखोल उत्तर विश्लेषण तयार करत आहे..."):
                test_prompt = f"Subject: {subject_selected}, Topic: {topic_selected}. Generate 1 Premium Multiple Choice Question (MCQ) matching exam standards (like NEET/JEE), give 4 options, state the Correct Answer, and provide a highly detailed step-by-step logical explanation/derivation so the student learns the mistake immediately."
                ans = fetch_ai_response(test_prompt, base_ai_instruction)
                st.markdown(f'<div class="glass-card" style="border-left: 5px solid #00ffcc;">{ans}</div>', unsafe_allow_html=True)

    # करिअर मार्गदर्शक
    with tab5:
        st.markdown(f"### {current_ui['tabs'][4]}")
        stream = st.selectbox(current_ui["sel5_lbl"], current_ui["streams"], key="stream")
        scope = st.radio(current_ui["rad5_lbl"], current_ui["scopes"], key="scope")
        interest = st.text_input(current_ui["txt5_lbl"], "Solar Energy / Software", key="interest")
        if st.button(current_ui["btn5_lbl"], key="btn5"):
            with st.spinner("मार्गदर्शन तयार होत आहे..."):
                st.write(fetch_ai_response(f"Stream: {stream}, Scope: {scope}, Core Interest: {interest}", base_ai_instruction + " Give concrete roadmap, modern jobs, and free learning pathways."))

    # भाषा केंद्र
    with tab6:
        st.markdown(f"### {current_ui['tabs'][5]}")
        st.success(f"✔️ Multilingual Synchronization Active for: {selected_display_lang}")

# ==========================================
# विभाग ३: स्वतंत्र थेट शंका निरसन केंद्र
# ==========================================
elif app_mode == "doubt":
    st.markdown(f'<span class="main-title">{current_ui["doubt_menu"]}</span>', unsafe_allow_html=True)
    user_query = st.text_area(current_ui["q1_lbl"], key="q1_direct", height=150)
    if st.button(current_ui["btn1_lbl"], key="btn1_direct"):
        with st.spinner("AI मार्गदर्शक उत्तर शोधत आहेत..."):
            ans = fetch_ai_response(user_query, base_ai_instruction + " Give direct, mathematically precise, and easy to understand solutions.")
            st.markdown(f'<div class="glass-card" style="border-left: 5px solid #FFD700; font-size:1.15rem;">{ans}</div>', unsafe_allow_html=True)

# ==========================================
# विभाग ४: लॉगिन / प्रोफाईल
# ==========================================
elif app_mode == "login":
    st.markdown(f'<span class="main-title">{current_ui["login_menu"]}</span>', unsafe_allow_html=True)
    with st.form("login_form"):
        st.text_input("Username / Email:")
        st.text_input("Password:", type="password")
        st.form_submit_button("Submit")

# --- ९. एकत्रित फायनल फुटर ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">Developed by Dnyaneshwar Gawalikar</p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem;">Professor & Head of Department</p>
        <p style="font-size: 0.8rem; color: #8b949e;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>
    </div>
""", unsafe_allow_html=True)
