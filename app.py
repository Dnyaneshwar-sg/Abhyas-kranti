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

# --- ३. ग्लोबल भाषा आणि राज्य मॅपिंग ---
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
    "Bengali (বাংলা) - पश्चिम बंगाल": "Bengali"
}

# --- ४. डाव्या बाजूच्या साईडबारसाठी विशेष सुपर हाय-कॉन्ट्रास्ट CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; }
    
    .stApp {
        background: #0d1117; 
        color: #f0f6fc !important; 
    }
    
    /* --- डाव्या बाजूच्या साईडबारचा जबरदस्त विजिबिलिटी मेकओव्हर --- */
    [data-testid="stSidebar"] {
        background-color: #070a0e !important; /* एकदम डार्क ब्लॅक पार्श्वभूमी */
        border-right: 3px solid #FFD700 !important; /* मुख्य स्क्रीन आणि साईडबार दरम्यान ठळक सोनेरी बॉर्डर */
        padding: 20px 10px;
    }
    
    /* साईडबार मधील मुख्य लेबल्स (खूप मोठे आणि चमकदार सोनेरी) */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFD700 !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        margin-bottom: 12px !important;
    }
    
    /* रेडिओ बटणांचे बॉक्स मोठे आणि स्पष्ट करणे */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div {
        background-color: #161b22 !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        border: 2px solid #30363d !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    
    /* रेडिओ मधील अक्षरे (शुद्ध पांढरी आणि ठळक) */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* सिलेक्टबॉक्स इनपुट डिझाईन */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* मुख्य स्क्रीनवरील इतर डिझाईन्स */
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
        font-size: 1.05rem;
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

# --- ५. डायनॅमिक इंटरफेस ट्रान्सलेशन मॅट्रिक्स (Dynamic UI System) ---
UI_LANG_MATRIX = {
    "Marathi": {
        "menu_lbl": "🌍 १. भाषा व राज्य निवडा (Select Language)",
        "nav_lbl": "📌 २. अभ्यास क्रांती मेनू",
        "dash_menu": "🏠 मुख्य पान (Dashboard)",
        "sandbox_menu": "⚡ AI प्रगत फीचर्स सँडबॉक्स",
        "tabs": ["🧠 शंका निरसन शिक्षक", "📅 अभ्यास वेळापत्रक", "🛡️ स्कॉलरशिप इंजिन", "🎯 परीक्षा केंद्र", "🛣️ करिअर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "तुमचा शैक्षणिक प्रश्न विचारा:",
        "btn1_lbl": "🚀 शंका निरसन करा",
        "q2_lbl": "कोणत्या परीक्षेची तयारी करत आहात?",
        "s2_lbl": "रोज अभ्यासासाठी किती तास उपलब्ध आहेत?",
        "btn2_lbl": "🚀 स्मार्ट वेळापत्रक तयार करा",
        "sel3_lbl": "विद्यार्थ्याची शैक्षणिक पातळी / इयत्ता निवडा:",
        "edu_opts": ["इयत्ता १ ली ते ४ थी (प्राथमिक शाळा)", "इयत्ता ५ वी ते ७ वी (उच्च प्राथमिक)", "इयत्ता ८ वी ते १० वी (माध्यमिक / SSC)", "इयत्ता ११ वी आणि १२ वी (ज्युनिअर कॉलेज / HSC)", "पदवी शिक्षण (Undergraduate)", "पदव्युत्तर शिक्षण (Postgraduate)", "पीएच.डी. आणि उच्च संशोधन", "जागतिक शिक्षण / परदेशातील उच्च शिक्षण"],
        "inc3_lbl": "कौटुंबिक वार्षिक उत्पन्न निवडा:",
        "inc_opts": ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाख ते ₹८ लाख", "₹८ लाखांपेक्षा जास्त"],
        "cat3_lbl": "प्रवर्ग / जात / आरक्षित श्रेणी (उदा. Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 पात्र स्कॉलरशिप शोधा",
        "sel4_lbl": "परीक्षेची पातळी निवडा:",
        "exam_tiers": ["राज्याची राज्य पातळीवरील परीक्षा (State PSC / Govt Exams)", "राष्ट्रीय पातळीवरील परीक्षा (UPSC, NEET, JEE, NDA)", "जागतिक / आंतरराष्ट्रीय परीक्षा (GRE, GMAT, IELTS, TOEFL)"],
        "txt4_lbl": "थेट परीक्षेचे नाव टाईप करा:",
        "btn4_lbl": "🚀 परीक्षा पॅटर्न व नमुना प्रश्न मिळवा",
        "sel5_lbl": "विद्याशाखा / प्रवाह निवडा (Select Stream):",
        "streams": ["कला शाखा (Arts & Humanities)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तांत्रिक व मेडिकल (Technical & Medical)", "व्यावसायिक व कौशल्य विकास (Vocational/Solar/Agri)"],
        "rad5_lbl": "करिअरची व्याप्ती (Scope):",
        "scopes": ["स्थानिक आणि राष्ट्रीय संधी (Local & National)", "जागतिक संधी (Global & International)"],
        "txt5_lbl": "विद्यार्थ्याची वैयक्तिक आवड (उदा. डेटा सायन्स, सोलर बिझनेस):",
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
        "sel3_lbl": "Select Educational Level / Grade:",
        "edu_opts": ["1st - 4th Grade (Primary)", "5th - 7th Grade (Upper Primary)", "8th - 10th Grade (Secondary/SSC)", "11th & 12th Grade (HSC)", "Undergraduate (BA, B.Sc, B.E, MBBS)", "Postgraduate (MA, M.Sc, MBA)", "Ph.D. & Advanced Research", "Global & International Studies"],
        "inc3_lbl": "Select Annual Family Income:",
        "inc_opts": ["Below ₹1.5 Lakhs", "₹1.5 Lakhs to ₹3 Lakhs", "₹3 Lakhs to ₹8 Lakhs", "Above ₹8 Lakhs"],
        "cat3_lbl": "Type Category / Reservation (e.g., Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 Find Eligible Scholarships",
        "sel4_lbl": "Select Examination Tier:",
        "exam_tiers": ["State Level Government Exams (PSC/State Boards)", "National Level Exams (UPSC, NEET, JEE, NDA)", "Global / International Exams (GRE, GMAT, IELTS)"],
        "txt4_lbl": "Type Target Exam Name:",
        "btn4_lbl": "🚀 Get Pattern & Sample Questions",
        "sel5_lbl": "Select Academic Stream:",
        "streams": ["Arts & Humanities", "Commerce & Management", "Pure & Applied Sciences", "Technical, Engineering & Medical", "Vocational & Skills (Solar, Tailoring, Agri)"],
        "rad5_lbl": "Career Scope Level:",
        "scopes": ["Local & National Opportunities", "Global & International Opportunities"],
        "txt5_lbl": "Your Core Area of Interest (e.g., Solar, Data Science):",
        "btn5_lbl": "🚀 Generate Career Roadmap & Links"
    },
    "Hindi": {
        "menu_lbl": "🌍 1. भाषा और राज्य चुनें",
        "nav_lbl": "📌 2. अभ्यास क्रांति मेनू",
        "dash_menu": "🏠 मुख्य डैशボード",
        "sandbox_menu": "⚡ AI एडवांस्ड सैंडबॉक्स",
        "tabs": ["🧠 शंका समाधान शिक्षक", "📅 अध्ययन समय-सारणी", "🛡️ स्कॉलरशिप इंजन", "🎯 परीक्षा केंद्र", "🛣️ करियर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "अपना शैक्षणिक प्रश्न पूछें:",
        "btn1_lbl": "🚀 शंका समाधान करें",
        "q2_lbl": "आप किस परीक्षा की तैयारी कर रहे हैं?",
        "s2_lbl": "रोजाना पढ़ाई के लिए कितने घंटे उपलब्ध हैं?",
        "btn2_lbl": "🚀 स्मार्ट समय-सारणी बनाएं",
        "sel3_lbl": "शैक्षणिक स्तर / कक्षा चुनें:",
        "edu_opts": ["कक्षा 1 से 4 (प्राथमिक)", "कक्षा 5 से 7 (उच्च प्राथमिक)", "कक्षा 8 से 10 (माध्यमिक/SSC)", "कक्षा 11 और 12 (HSC)", "स्नातक (Undergraduate)", "स्नातकोत्तर (Postgraduate)", "पीएच.डी. और उच्च अनुसंधान", "वैश्विक शिक्षा / विदेश में उच्च शिक्षा"],
        "inc3_lbl": "वार्षिक पारिवारिक आय चुनें:",
        "inc_opts": ["₹1.5 लाख से कम", "₹1.5 लाख से ₹3 लाख", "₹3 लाख से ₹8 लाख", "₹8 लाख से अधिक"],
        "cat3_lbl": "अपनी श्रेणी / जाति टाइप करें (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 योग्य स्कॉलरशिप खोजें",
        "sel4_lbl": "परीक्षा का स्तर चुनें:",
        "exam_tiers": ["राज्य स्तरीय सरकारी परीक्षा (State PSC)", "राष्ट्रीय स्तरीय परीक्षा (UPSC, NEET, JEE)", "वैश्विक / अंतर्राष्ट्रीय परीक्षा (GRE, GMAT, IELTS)"],
        "txt4_lbl": "परीक्षा का नाम टाइप करें:",
        "btn4_lbl": "🚀 परीक्षा पैटर्न और प्रश्न प्राप्त करें",
        "sel5_lbl": "शैक्षणिक स्ट्रीम/शाखा चुनें:",
        "streams": ["कला शाखा (Arts & Humanities)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तकनीकी और मेडिकल (Technical & Medical)", "व्यावसायिक और कौशल (Vocational/Solar)"],
        "rad5_lbl": "करियर का दायरा:",
        "scopes": ["स्थानीय और राष्ट्रीय अवसर", "वैश्विक अवसर (Global Opportunities)"],
        "txt5_lbl": "अपनी व्यक्तिगत रुचि टाइप करें (जैसे सोलर, डेटा साइंस):",
        "btn5_lbl": "🚀 करियर रोडमॅप और लिंक्स प्राप्त करें"
    }
}

# --- ६. डाव्या साईडबार इंटरफेसचे सादरीकरण (पहिले भाषा लोड करणे जेणेकरून त्रुटी येणार नाही) ---
if "global_language_selector" in st.session_state:
    temp_lang = languages_map[st.session_state["global_language_selector"]]
    sidebar_ui = UI_LANG_MATRIX.get(temp_lang, UI_LANG_MATRIX["English"])
else:
    sidebar_ui = UI_LANG_MATRIX["Marathi"] # पहिली डिफॉल्ट भाषा

selected_display_lang = st.sidebar.selectbox(
    sidebar_ui["menu_lbl"],
    list(languages_map.keys()),
    key="global_language_selector"
)
target_lang = languages_map[selected_display_lang]

# निवडलेल्या भाषेनुसार संपूर्ण UI मॅट्रिक्स अपडेट करणे
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

app_mode = st.sidebar.radio(current_ui["nav_lbl"], [current_ui["dash_menu"], current_ui["sandbox_menu"]])

# --- ७. AI कॉल फंक्शन (Groq API) ---
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

# AI इंजिनसाठी युनिवर्सल प्रादेशिक प्रॉम्ट
base_ai_instruction = f"""
You are the elite AI Engine of 'Abhyas Kranti' App, adapted for {target_lang}.
CRITICAL MANDATE:
1. You MUST generate your entire response exclusively in the language: '{target_lang}'.
2. You must align all answers, rules, and logic precisely with the specific state rules associated with '{selected_display_lang}' (e.g. State board patterns, state scholarship quotas, regional career trends).
"""

# ==========================================
# विभाग १: मुख्य पान (Dashboard)
# ==========================================
if app_mode == current_ui["dash_menu"]:
    st.markdown('<span class="main-title">Abhyas Kranti National Portal</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown(f"**🌍 Active System Rules & Language Context:** `{selected_display_lang}`")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="glass-card"><h4>Resource Fragmentation</h4><p style="color:#c9d1d9;">Lack of centralized resources solved via unified multilingual UI.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="glass-card"><h4>Language Barriers</h4><p style="color:#c9d1d9;">Bypassed using real-time dynamic interface translations across 22 languages.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="glass-card"><h4>Information Asymmetry</h4><p style="color:#c9d1d9;">State-specific criteria, reservations, and schemes matched dynamically.</p></div>', unsafe_allow_html=True)

# ==========================================
# विभाग २: AI प्रगत फीचर्स सँडबॉक्स (6-in-1 Live Dynamic Engine)
# ==========================================
elif app_mode == current_ui["sandbox_menu"]:
    st.title("⚡ AI Action Sandbox")
    st.markdown(f"##### 🌍 Current Language Matrix: `{selected_display_lang}`")

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
        edu_level = st.selectbox(current_ui["sel3_lbl"], current_ui["edu_opts"], key="edu_lvl")
        income_level = st.selectbox(current_ui["inc3_lbl"], current_ui["inc_opts"], key="inc_lvl")
        category = st.text_input(current_ui["cat3_lbl"], "OBC", key="cat")
        if st.button(current_ui["btn3_lbl"], key="btn3"):
            with st.spinner("Scanning State & International Scholarship Rules..."):
                query = f"Level: {edu_level}, Income: {income_level}, Category: {category}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide 3 best scholarships (State-specific, National or Global) with official eligibility rules, text in the chosen language.")
                st.write(ai_response)

    # --- TAB 4: Competitive Exams (State, National & Global) ---
    with tab4:
        st.markdown(f"### {current_ui['tabs'][3]}")
        exam_level = st.selectbox(current_ui["sel4_lbl"], current_ui["exam_tiers"], key="ex_lvl")
        specific_exam = st.text_input(current_ui["txt4_lbl"], "PSC Exam", key="spec_ex")
        if st.button(current_ui["btn4_lbl"], key="btn4"):
            with st.spinner("Fetching Exam Blueprints..."):
                query = f"Tier: {exam_level}, Exam: {specific_exam}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide the latest structure, changes, and 1 high-yield sample MCQ with explanation in the chosen language.")
                st.write(ai_response)

    # --- TAB 5: Career Guidance (All Streams + Resource Links) ---
    with tab5:
        st.markdown(f"### {current_ui['tabs'][4]}")
        academic_stream = st.selectbox(current_ui["sel5_lbl"], current_ui["streams"], key="stream")
        career_scope = st.radio(current_ui["rad5_lbl"], current_ui["scopes"], key="scope")
        specific_interest = st.text_input(current_ui["txt5_lbl"], "Solar Energy & Automation", key="interest")
        if st.button(current_ui["btn5_lbl"], key="btn5"):
            with st.spinner("Mapping Career Paths..."):
                query = f"Stream: {academic_stream}, Scope: {career_scope}, Interest: {specific_interest}"
                ai_response = fetch_ai_response(query, base_ai_instruction + "Provide 3 futuristic career options. MANDATORY: Include clickable official resource links in markdown format [Website Name](URL). Text must be in the chosen language.")
                st.write(ai_response)

    # --- TAB 6: Language Dashboard ---
    with tab6:
        st.markdown(f"### {current_ui['tabs'][5]}")
        st.success(f"✔️ Active Language Target Context: **{selected_display_lang}**")
        st.info("The entire UI text, drop-downs, labels, and underlying state configurations are now synchronized dynamically.")

# --- ८. एकत्रित फायनल फुटर ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">Developed by Dnyaneshwar Gawalikar</p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem;">Professor & Head of Department</p>
        <p style="font-size: 0.8rem; color: #8b949e;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>
    </div>
""", unsafe_allow_html=True)
