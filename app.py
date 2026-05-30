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
    page_title="Abhyas Kranti National - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ३. ग्लोबल भाषा मॅपिंग (English समाविष्ट करून) ---
languages_map = {
    "मराठी (Marathi) - महाराष्ट्र": "Marathi",
    "English - Pan India": "English",
    "हिंदी (Hindi) - उत्तर प्रदेश / बिहार / दिल्ली": "Hindi",
    "Gujarati (ગુજરાતી) - गुजरात": "Gujarati",
    "Kannada (ಕನ್ನಡ) - कर्नाटक": "Kannada",
    "Tamil (தமிழ்) - तमिळनाडू": "Tamil",
    "Telugu (తెలుగు) - आंध्र / तेलंगणा": "Telugu",
    "Malayalam (മലയാളം) - केरळ": "Malayalam",
    "Punjabi (ਪੰਜਾਬੀ) - पंजाब": "Punjabi",
    "Bengali (বাংলা) - पश्चिम बंगाल": "Bengali",
    "Urdu (اردو)": "Urdu",
    "Sanskrit (संस्कृतम्)": "Sanskrit",
    "Konkani (कोंकणी) - गोवा": "Konkani",
    "Assamese (অসমীয়া) - आसाम": "Assamese",
    "Oriya (ଓଡ଼ିଆ) - ओडिशा": "Oriya",
    "Kashmiri (कश्मीरी)": "Kashmiri",
    "Nepali (नेपाली)": "Nepali",
    "Sindhi (सिंधी)": "Sindhi",
    "Manipuri (মণিপুরী)": "Manipuri",
    "Bodo (बोडो)": "Bodo",
    "Dogri (डोगरी)": "Dogri",
    "Maithili (मैथिली) - बिहार": "Maithili",
    "Santali (संथाली)": "Santali"
}

# --- ४. डाव्या बाजूच्या साईडबारसाठी विशेष हाय-विजिबिलिटी आणि प्रीमियम डार्क CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; }
    
    .stApp {
        background: #0d1117; 
        color: #f0f6fc !important; 
    }
    
    /* --- डाव्या बाजूच्या साईडबारसाठी उत्कृष्ट विजिबिलिटी फिक्स --- */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important; /* फिकट काळा उठून दिसणारा रंग */
        border-right: 2px solid #30363d;
        padding-top: 20px;
    }
    
    /* साईडबारमधील मजकूर मोठा, स्पष्ट आणि ठळक करण्यासाठी */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    /* साईडबार मधील रेडिओ ऑप्शन्सना बॉक्समध्ये रूपांतरित करणे (बारीक पाहावे लागणार नाही) */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div {
        background-color: #21262d !important;
        padding: 12px 15px !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid #30363d !important;
        transition: all 0.2s ease;
    }
    
    /* सिलेक्ट केलेल्या बॉक्सला हायलाईट करणे */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div:hover {
        border-color: #FFD700 !important;
        background-color: #262c36 !important;
    }
    
    /* ड्रॉपडाऊन सिलेक्टबॉक्स डिझाईन */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #21262d !important;
        border: 2px solid #ffde59 !important;
        border-radius: 8px !important;
    }

    /* मुख्य स्क्रीन हेडर्स आणि टॅब्स */
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        display: block;
    }
    
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-weight: 700 !important; }
    
    .glass-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #21262d;
        border-radius: 6px;
        color: #c9d1d9 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #0d1117 !important; 
        font-weight: 700 !important;
    }
    
    .footer-container {
        border-top: 1px solid #30363d;
        padding-top: 25px;
        margin-top: 50px;
        text-align: center;
        color: #8b949e;
    }
    </style>
""", unsafe_allow_html=True)

# --- ५. डायनॅमिक इंटरफेस ट्रान्सलेशन मॅट्रिक्स (Dynamic UI Dictionary) ---
UI_LANG_MATRIX = {
    "Marathi": {
        "menu_lbl": "🌍 १. भाषा व राज्य निवडा",
        "nav_lbl": "📌 २. अभ्यास क्रांती मेनू",
        "dash_menu": "🏠 मुख्य पान (Dashboard)",
        "sandbox_menu": "⚡ AI प्रगत फीचर्स सँडबॉक्स",
        "tabs": ["🧠 शंका निरसन शिक्षक", "📅 अभ्यास वेळापत्रक", "🛡️ स्कॉलरशिप इंजिन", "🎯 परीक्षा केंद्र", "🛣️ करिअर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "तुमचा शैक्षणिक प्रश्न विचारा:",
        "btn1_lbl": "🚀 शंका निरसन करा",
        "q2_lbl": "कोणत्या परीक्षेची तयारी करत आहात?",
        "s2_lbl": "रोज अभ्यासासाठी किती तास उपलब्ध आहेत?",
        "btn2_lbl": "🚀 स्मार्ट वेळापत्रक तयार करा",
        "sel3_lbl": "शैक्षणिक पातळी निवडा:",
        "inc3_lbl": "वार्षिक उत्पन्न निवडा:",
        "cat3_lbl": "तुमचा प्रवर्ग/जात टाईप करा:",
        "btn3_lbl": "🚀 पात्र स्कॉलरशिप शोधा",
        "sel4_lbl": "परीक्षेची पातळी निवडा:",
        "txt4_lbl": "थेट परीक्षेचे नाव टाईप करा:",
        "btn4_lbl": "🚀 परीक्षा पॅटर्न व प्रश्न मिळवा",
        "sel5_lbl": "विद्याशाखा / प्रवाह निवडा:",
        "rad5_lbl": "करिअरची व्याप्ती:",
        "txt5_lbl": "तुमची वैयक्तिक आवड:",
        "btn5_lbl": "🚀 करिअर रोडमॅप व लिंक्स मिळवा"
    },
    "English": {
        "menu_lbl": "🌍 1. Select Language & State",
        "nav_lbl": "📌 2. Abhyas Kranti Menu",
        "dash_menu": "🏠 Main Dashboard",
        "sandbox_menu": "⚡ AI Advanced Sandbox",
        "tabs": ["🧠 Doubt Solver", "📅 Study Planner", "🛡️ Scholarship Engine", "🎯 Exam Center", "🛣️ Career Guide", "🌐 Language Hub"],
        "q1_lbl": "Ask your academic question here:",
        "btn1_lbl": "🚀 Solve My Doubt",
        "q2_lbl": "Which exam are you preparing for?",
        "s2_lbl": "How many hours can you study daily?",
        "btn2_lbl": "🚀 Create Smart Schedule",
        "sel3_lbl": "Select Educational Level:",
        "inc3_lbl": "Select Annual Family Income:",
        "cat3_lbl": "Type your Category/Caste:",
        "btn3_lbl": "🚀 Find Eligible Scholarships",
        "sel4_lbl": "Select Exam Tier:",
        "txt4_lbl": "Type Target Exam Name:",
        "btn4_lbl": "🚀 Get Pattern & Sample Questions",
        "sel5_lbl": "Select Academic Stream:",
        "rad5_lbl": "Career Scope Level:",
        "txt5_lbl": "Your Core Area of Interest:",
        "btn5_lbl": "🚀 Generate Career Roadmap & Links"
    },
    "Hindi": {
        "menu_lbl": "🌍 1. भाषा और राज्य चुनें",
        "nav_lbl": "📌 2. अभ्यास क्रांति मेनू",
        "dash_menu": "🏠 मुख्य डैशबोर्ड (Dashboard)",
        "sandbox_menu": "⚡ AI एडवांस्ड सैंडबॉक्स",
        "tabs": ["🧠 शंका समाधान शिक्षक", "📅 अध्ययन समय-सारणी", "🛡️ स्कॉलरशिप इंजन", "🎯 परीक्षा केंद्र", "🛣️ करियर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "अपना शैक्षणिक प्रश्न पूछें:",
        "btn1_lbl": "🚀 शंका समाधान करें",
        "q2_lbl": "आप किस परीक्षा की तैयारी कर रहे हैं?",
        "s2_lbl": "रोजाना पढ़ाई के लिए कितने घंटे उपलब्ध हैं?",
        "btn2_lbl": "🚀 स्मार्ट समय-सारणी बनाएं",
        "sel3_lbl": "शैक्षणिक स्तर चुनें:",
        "inc3_lbl": "वार्षिक पारिवारिक आय चुनें:",
        "cat3_lbl": "अपनी श्रेणी/जाति टाइप करें:",
        "btn3_lbl": "🚀 योग्य स्कॉलरशिप खोजें",
        "sel4_lbl": "परीक्षा का स्तर चुनें:",
        "txt4_lbl": "परीक्षा का नाम टाइप करें:",
        "btn4_lbl": "🚀 परीक्षा पैटर्न और प्रश्न प्राप्त करें",
        "sel5_lbl": "शैक्षणिक स्ट्रीम/शाखा चुनें:",
        "rad5_lbl": "करियर का दायरा:",
        "txt5_lbl": "आपकी व्यक्तिगत रुचि:",
        "btn5_lbl": "🚀 करियर रोडमॅप और लिंक्स प्राप्त करें"
    }
}

# अन्य सर्व २0 भाषांसाठी डिफॉल्ट फॉलबॅक (Fallback Setup)
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

# --- ६. साईडबार इंटरफेस ---
selected_display_lang = st.sidebar.selectbox(
    current_ui["menu_lbl"],
    list(languages_map.keys()),
    key="global_language_selector"
)
target_lang = languages_map[selected_display_lang]

# भाषा बदलल्यास UI री-लोड करणे
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

app_mode = st.sidebar.radio(current_ui["nav_lbl"], [current_ui["dash_menu"], current_ui["sandbox_menu"]])

# AI इंजिनसाठी युनिवर्सल प्रॉम्ट
base_ai_instruction = f"""
You are the elite AI Engine of 'Abhyas Kranti' App, adapted for {target_lang}.
CRITICAL MANDATE:
1. You MUST generate your entire response exclusively in the language: '{target_lang}'.
2. You must align all answers, rules, and logic precisely with the specific state rules associated with '{selected_display_lang}' (e.g. State board patterns, state scholarship quotas, regional career trends).
"""

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

# ==========================================
# विभाग १: मुख्य पान (Dashboard)
# ==========================================
if app_mode == current_ui["dash_menu"]:
    st.markdown('<span class="main-title">Abhyas Kranti Ultimate</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown(f"**🌍 Active System Rules & Language:** `{selected_display_lang}`")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="glass-card"><h4>Resource Fragmentation</h4><p style="color:#c9d1d9;">Lack of centralized resources solved via unified UI.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="glass-card"><h4>Language Barriers</h4><p style="color:#c9d1d9;">Bypassed using real-time dynamic interface translations.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="glass-card"><h4>Information Gap</h4><p style="color:#c9d1d9;">State-specific criteria matched dynamically.</p></div>', unsafe_allow_html=True)

# ==========================================
# विभाग २: AI प्रगत फीचर्स सँडबॉक्स (6-in-1 Live Dynamic Engine)
# ==========================================
elif app_mode == current_ui["sandbox_menu"]:
    st.title("⚡ AI Action Sandbox")
    st.markdown(f"##### 🌍 Current Engine Interface Context: `{selected_display_lang}`")

    # डायनॅमिक टॅब नेम्स जे निवडलेल्या भाषेनुसार बदलतात
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(current_ui["tabs"])

    # --- TAB 1: Doubt Solving ---
    with tab1:
        st.markdown(f"### {current_ui['tabs'][0]}")
        user_query = st.text_input(current_ui["q1_lbl"], key="q1")
        if st.button(current_ui["btn1_lbl"], key="btn1"):
            with st.spinner("AI Engine Processing..."):
                ai_response = fetch_ai_response(user_query, base_ai_instruction + "Answer the query clearly with bullet points in the selected language.")
                st.write(ai_response)

    # --- TAB 2: Study Planner ---
    with tab2:
        st.markdown(f"### {current_ui['tabs'][1]}")
        exam_target = st.text_input(current_ui["q2_lbl"], "Board Exams", key="q2")
        available_hours = st.slider(current_ui["s2_lbl"], 1, 12, 5, key="s2")
        if st.button(current_ui["btn2_lbl"], key="btn2"):
            with st.spinner("Generating Planner..."):
                query = f"Exam: {exam_target}, Hours: {available_hours}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Design a detailed 7-day study plan in the chosen language.")
                st.write(ai_response)

    # --- TAB 3: Scholarship Engine (1st to Global + State Rules) ---
    with tab3:
        st.markdown(f"### {current_ui['tabs'][2]}")
        edu_level = st.selectbox(current_ui["sel3_lbl"], ["1st - 4th Grade", "5th - 10th Grade", "11th - 12th (HSC)", "Undergraduate (UG)", "Postgraduate (PG)", "Ph.D. Research", "Global/International Studies"], key="edu_lvl")
        income_level = st.selectbox(current_ui["inc3_lbl"], ["< 1.5 Lakhs", "1.5L - 3L", "3L - 8L", "> 8 Lakhs"], key="inc_lvl")
        category = st.text_input(current_ui["cat3_lbl"], "General/OBC", key="cat")
        if st.button(current_ui["btn3_lbl"], key="btn3"):
            with st.spinner("Scanning State & International Scholarship Rules..."):
                query = f"Level: {edu_level}, Income: {income_level}, Category: {category}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide 3 best scholarships (State-specific, National or Global) with official eligibility rules, text in the chosen language.")
                st.write(ai_response)

    # --- TAB 4: Competitive Exams (State, National & Global) ---
    with tab4:
        st.markdown(f"### {current_ui['tabs'][3]}")
        exam_level = st.selectbox(current_ui["sel4_lbl"], ["State Government/PSC Exams", "National Level Exams (UPSC, NEET, JEE)", "International Exams (GRE, GMAT, IELTS)"], key="ex_lvl")
        specific_exam = st.text_input(current_ui["txt4_lbl"], "State PSC", key="spec_ex")
        if st.button(current_ui["btn4_lbl"], key="btn4"):
            with st.spinner("Fetching Exam Blueprints..."):
                query = f"Tier: {exam_level}, Exam: {specific_exam}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide the latest structure, changes, and 1 high-yield sample MCQ with explanation in the chosen language.")
                st.write(ai_response)

    # --- TAB 5: Career Guidance (All Streams + Resource Links) ---
    with tab5:
        st.markdown(f"### {current_ui['tabs'][4]}")
        academic_stream = st.selectbox(current_ui["sel5_lbl"], ["Arts & Humanities", "Commerce & Management", "Pure Sciences", "Engineering & Medical", "Vocational & Skills (Solar, Agriculture, Digital)"], key="stream")
        career_scope = st.radio(current_ui["rad5_lbl"], ["Local & National Opportunities", "Global/International Opportunities"], key="scope")
        specific_interest = st.text_input(current_ui["txt5_lbl"], "Automation & Technology", key="interest")
        if st.button(current_ui["btn5_lbl"], key="btn5"):
            with st.spinner("Mapping Career Paths..."):
                query = f"Stream: {academic_stream}, Scope: {career_scope}, Interest: {specific_interest}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide 3 futuristic career options. MANDATORY: Include clickable official resource links in markdown format [Website](URL). Text must be in the chosen language.")
                st.write(ai_response)

    # --- TAB 6: Language Dashboard ---
    with tab6:
        st.markdown(f"### {current_ui['tabs'][5]}")
        st.success(f"✔️ Active Language Target Context: **{selected_display_lang}**")
        st.info("The entire UI text, labels, and underlying state configurations are now synchronized dynamically.")

# --- ७. एकत्रित फायनल फुटर ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">Developed by Dnyaneshwar Gawalikar</p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem;">Professor & Head of Department</p>
        <p style="font-size: 0.8rem; color: #8b949e;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>
    </div>
""", unsafe_allow_html=True)
