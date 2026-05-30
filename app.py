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
    "Kannada (ಕನ್ನಡ) - कर्नाटक": "Kannada",
    "Tamil (தமிழ்) - तमिळનાડુ": "Tamil",
    "Telugu (తెలుగు) - આંધ્ર / તેલંગણા": "Telugu",
    "Punjabi (ਪੰਜਾਬੀ) - પંજાબ": "Punjabi",
    "Bengali (বাংলা) - પશ્ચિમ બંગાળ": "Bengali"
}

# --- ४. डायनॅमिक इंटरफेस ट्रान्सलेशन मॅट्रिक्स (मराठी, इंग्रजी, हिंदी, गुजराती समाविष्ट) ---
UI_LANG_MATRIX = {
    "Marathi": {
        "menu_lbl": "🌍 १. भाषा व राज्य निवडा (Select Language)",
        "nav_lbl": "📌 २. मुख्य विभाग (Navigation Menu)",
        "dash_menu": "🏠 मुख्य पान (Dashboard)",
        "sandbox_menu": "⚡ ६-इन-१ AI सँडबॉक्स",
        "doubt_menu": "🧠 स्वतंत्र शंका निरसन केंद्र",
        "login_menu": "🔐 लॉगिन / प्रोफाईल",
        "tabs": ["🧠 शंका निरसन शिक्षक", "📅 अभ्यास वेळापत्रक", "🛡️ स्कॉलरशिप इंजिन", "🎯 परीक्षा केंद्र", "🛣️ करिअर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "तुमचा शैक्षणिक प्रश्न विचारा:",
        "btn1_lbl": "🚀 शंका निरसन करा",
        "q2_lbl": "कोणत्या परीक्षेची तयारी करत आहात?",
        "s2_lbl": "रोज अभ्यासासाठी किती तास उपलब्ध आहेत?",
        "btn2_lbl": "🚀 स्मार्ट वेळापत्रक तयार करा",
        "sel3_lbl": "विद्यार्थ्याची शैक्षणिक पातळी / इयत्ता निवडा:",
        "edu_opts": ["इयत्ता १ ली ते ४ थी (प्राथमिक शाळा)", "इयत्ता ५ वी ते ७ वी (उच्च प्राथमिक)", "इयत्ता ८ वी ते १० वी (SSC)", "इयत्ता ११ वी आणि १२ वी (HSC)", "पदवी शिक्षण (Undergraduate)", "पदव्युत्तर शिक्षण (Postgraduate)", "पीएच.डी. आणि उच्च संशोधन", "जागतिक शिक्षण / परदेशातील उच्च शिक्षण"],
        "inc3_lbl": "कौटुंबिक वार्षिक उत्पन्न निवडा:",
        "inc_opts": ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाख ते ₹८ लाख", "₹८ लाखांपेक्षा जास्त"],
        "cat3_lbl": "प्रवर्ग / जात / आरक्षित श्रेणी (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 पात्र स्कॉलरशिप शोधा",
        "sel4_lbl": "परीक्षेची पातळी निवडा:",
        "exam_tiers": ["राज्याची राज्य पातळीवरील परीक्षा (State PSC)", "राष्ट्रीय पातळीवरील परीक्षा (UPSC, NEET, JEE, NDA)", "जागतिक / आंतरराष्ट्रीय परीक्षा (GRE, IELTS)"],
        "txt4_lbl": "थेट परीक्षेचे नाव टाईप करा:",
        "btn4_lbl": "🚀 परीक्षा पॅटर्न व नमुना प्रश्न मिळवा",
        "sel5_lbl": "विद्याशाखा / प्रवाह निवडा (Select Stream):",
        "streams": ["कला शाखा (Arts)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तांत्रिक व मेडिकल (Technical/Medical)", "व्यावसायिक व कौशल्य विकास (Vocational/Solar)"],
        "rad5_lbl": "करिअरची व्याप्ती (Scope):",
        "scopes": ["स्थानिक आणि राष्ट्रीय संधी (Local & National)", "जागतिक संधी (Global & International)"],
        "txt5_lbl": "विद्यार्थ्याची वैयक्तिक आवड (उदा. डेटा सायन्स, सोलर बिझनेस):",
        "btn5_lbl": "🚀 करिअर रोडमॅप व लिंक्स मिळवा"
    },
    "English": {
        "menu_lbl": "🌍 1. Select Language & State",
        "nav_lbl": "📌 2. Navigation Menu",
        "dash_menu": "🏠 Main Dashboard",
        "sandbox_menu": "⚡ 6-in-1 AI Sandbox",
        "doubt_menu": "🧠 Direct Doubt Solver",
        "login_menu": "🔐 Login / Profile",
        "tabs": ["🧠 Doubt Solver", "📅 Study Planner", "🛡️ Scholarship Engine", "🎯 Exam Center", "🛣️ Career Guide", "🌐 Language Hub"],
        "q1_lbl": "Ask your academic question here:",
        "btn1_lbl": "🚀 Solve My Doubt",
        "q2_lbl": "Which exam are you preparing for?",
        "s2_lbl": "How many hours can you study daily?",
        "btn2_lbl": "🚀 Create Smart Schedule",
        "sel3_lbl": "Select Educational Level / Grade:",
        "edu_opts": ["1st - 4th Grade", "5th - 7th Grade", "8th - 10th Grade (SSC)", "11th & 12th Grade (HSC)", "Undergraduate", "Postgraduate", "Ph.D. Research", "Global & International Studies"],
        "inc3_lbl": "Select Annual Family Income:",
        "inc_opts": ["Below ₹1.5 Lakhs", "₹1.5 Lakhs to ₹3 Lakhs", "₹3 Lakhs to ₹8 Lakhs", "Above ₹8 Lakhs"],
        "cat3_lbl": "Type Category / Reservation (e.g., Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 Find Eligible Scholarships",
        "sel4_lbl": "Select Examination Tier:",
        "exam_tiers": ["State Level Exams (PSC)", "National Level Exams (UPSC, NEET, JEE)", "Global / International Exams (GRE, IELTS)"],
        "txt4_lbl": "Type Target Exam Name:",
        "btn4_lbl": "🚀 Get Pattern & Sample Questions",
        "sel5_lbl": "Select Academic Stream:",
        "streams": ["Arts & Humanities", "Commerce & Management", "Pure & Applied Sciences", "Technical & Medical", "Vocational & Skills (Solar, Agri)"],
        "rad5_lbl": "Career Scope Level:",
        "scopes": ["Local & National Opportunities", "Global Opportunities"],
        "txt5_lbl": "Your Core Area of Interest (e.g., Solar, Data Science):",
        "btn5_lbl": "🚀 Generate Career Roadmap & Links"
    },
    "Hindi": {
        "menu_lbl": "🌍 1. भाषा और राज्य चुनें",
        "nav_lbl": "📌 2. मुख्य मेनू (Navigation Menu)",
        "dash_menu": "🏠 मुख्य डैशबोर्ड",
        "sandbox_menu": "⚡ 6-इन-1 AI सैंडबॉक्स",
        "doubt_menu": "🧠 शंका समाधान केंद्र",
        "login_menu": "🔐 लॉगिन / प्रोफाइल",
        "tabs": ["🧠 शंका समाधान शिक्षक", "📅 अध्ययन समय-सारणी", "🛡️ स्कॉलरशिप इंजन", "🎯 परीक्षा केंद्र", "🛣️ करियर मार्गदर्शक", "🌐 भाषा केंद्र"],
        "q1_lbl": "अपना शैक्षणिक प्रश्न पूछें:",
        "btn1_lbl": "🚀 शंका समाधान करें",
        "q2_lbl": "आप किस परीक्षा की तैयारी कर रहे हैं?",
        "s2_lbl": "रोजाना पढ़ाई के लिए कितने घंटे उपलब्ध हैं?",
        "btn2_lbl": "🚀 स्मार्ट समय-सारणी बनाएं",
        "sel3_lbl": "शैक्षणिक स्तर / कक्षा चुनें:",
        "edu_opts": ["कक्षा 1 से 4", "कक्षा 5 से 7", "कक्षा 8 से 10 (SSC)", "कक्षा 11 और 12 (HSC)", "स्नातक (Undergraduate)", "स्नातकोत्तर (Postgraduate)", "पीएच.डी. अनुसंधान", "वैश्विक शिक्षा / विदेश में शिक्षा"],
        "inc3_lbl": "वार्षिक पारिवारिक आय चुनें:",
        "inc_opts": ["₹1.5 लाख से कम", "₹1.5 लाख से ₹3 लाख", "₹3 लाख से ₹8 लाख", "₹8 लाख से अधिक"],
        "cat3_lbl": "अपनी श्रेणी / जाति (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 योग्य स्कॉलरशिप खोजें",
        "sel4_lbl": "परीक्षा का स्तर चुनें:",
        "exam_tiers": ["राज्य स्तरीय परीक्षा (State PSC)", "राष्ट्रीय स्तरीय परीक्षा (UPSC, NEET, JEE)", "वैश्विक / अंतर्राष्ट्रीय परीक्षा (GRE, IELTS)"],
        "txt4_lbl": "परीक्षा का नाम टाइप करें:",
        "btn4_lbl": "🚀 परीक्षा पैटर्न और प्रश्न प्राप्त करें",
        "sel5_lbl": "शैक्षणिक स्ट्रीम/शाखा चुनें:",
        "streams": ["कला शाखा (Arts)", "वाणिज्य शाखा (Commerce)", "विज्ञान शाखा (Pure Sciences)", "तकनीकी और मेडिकल", "व्यावसायिक और कौशल (Vocational/Solar)"],
        "rad5_lbl": "करियर का दायरा:",
        "scopes": ["स्थानीय और राष्ट्रीय अवसर", "वैश्विक अवसर"],
        "txt5_lbl": "अपनी व्यक्तिगत रुचि (जैसे सोलर, डेटा साइंस):",
        "btn5_lbl": "🚀 करियर रोडमॅप और लिंक्स प्राप्त करें"
    },
    "Gujarati": {
        "menu_lbl": "🌍 1. ભાષા અને રાજ્ય પસંદ કરો",
        "nav_lbl": "📌 2. મુખ્ય મેનુ (Navigation Menu)",
        "dash_menu": "🏠 મુખ્ય પૃષ્ઠ (Dashboard)",
        "sandbox_menu": "⚡ 6-ઇન-1 AI સેન્ડબોક્સ",
        "doubt_menu": "🧠 શંકા નિવારણ કેન્દ્ર",
        "login_menu": "🔐 લોગિન / પ્રોફાઇલ",
        "tabs": ["🧠 શંકા નિવારણ શિક્ષક", "📅 અભ્યાસ સમયપત્રક", "🛡️ સ્કોલરશિપ એન્જિન", "🎯 પરીક્ષા કેન્દ્ર", "🛣️ કરિયર માર્ગદર્શક", "🌐 ભાષા કેન્દ્ર"],
        "q1_lbl": "તમારો શૈક્ષણિક પ્રશ્ન અહીં પૂછો:",
        "btn1_lbl": "🚀 શંકાનું સમાધાન કરો",
        "q2_lbl": "તમે કઈ પરીક્ષાની તૈયારી કરી રહ્યા છો?",
        "s2_lbl": "રોજ અભ્યાસ માટે કેટલા કલાક ઉપલબ્ધ છે?",
        "btn2_lbl": "🚀 સ્માર્ટ સમયપત્રક બનાવો",
        "sel3_lbl": "વિદ્યાર્થીનું શૈક્ષણિક સ્તર / ધોરણ પસંદ કરો:",
        "edu_opts": ["ધોરણ 1 થી 4 (પ્રાથમિક)", "ધોરણ 5 થી 7 (ઉચ્ચ પ્રાથમિક)", "ધોરણ 8 થી 10 (SSC)", "ધોરણ 11 અને 12 (HSC)", "સ્નાતક (Undergraduate)", "અનુસ્નાતક (Postgraduate)", "પીએચ.ડી. અને સંશોધન", "વૈશ્વિક શિક્ષણ / વિદેશમાં અભ્યાસ"],
        "inc3_lbl": "કૌટુંબિક વાર્ષિક આવક પસંદ કરો:",
        "inc_opts": ["₹1.5 લાખથી ઓછી", "₹1.5 લાખથી ₹3 લાખ", "₹3 લાખથી ₹8 લાખ", "₹8 લાખથી વધુ"],
        "cat3_lbl": "કેટેગરી / જાતિ ટાઈપ કરો (Open, OBC, SC, ST):",
        "btn3_lbl": "🚀 યોગ્ય સ્કોલરશિપ શોધો",
        "sel4_lbl": "પરીક્ષાનું સ્તર પસંદ કરો:",
        "exam_tiers": ["રાજ્ય સ્તરની સરકારી પરીક્ષા (State PSC)", "રાષ્ટ્રીય સ્તરની પરીક્ષા (UPSC, NEET, JEE)", "વૈશ્વિક / આંતરરાષ્ટ્રીય પરીક્ષા (GRE, IELTS)"],
        "txt4_lbl": "પરીક્ષાનું નામ ટાઈપ કરો:",
        "btn4_lbl": "🚀 પરીક્ષા પેટર્ન અને પ્રશ્નો મેળવો",
        "sel5_lbl": "શૈક્ષણિક પ્રવાહ પસંદ કરો (Select Stream):",
        "streams": ["આર્ટસ પ્રવાહ (Arts)", "કોમર્સ પ્રવાહ (Commerce)", "સાયન્સ પ્રવાહ (Pure Sciences)", "ટેકનિકલ અને મેડિકલ", "વ્યવસાયિક અને કૌશલ્ય (Vocational/Solar)"],
        "rad5_lbl": "કરિયર ક્ષેત્ર (Scope):",
        "scopes": ["સ્થાનિક અને રાષ્ટ્રીય તકો", "વૈશ્વિક તકો (Global Opportunities)"],
        "txt5_lbl": "વિદ્યાર્થીની વ્યક્તિગત રુચિ (જેમ કે સોલર, ડેટા સાયન્સ):",
        "btn5_lbl": "🚀 કરિયર રોડમેપ અને લિંક્સ મેળવો"
    }
}

# --- ५. प्रगत स्टायलिंग CSS (सुपर हाय-कॉन्ट्रास्ट विजिबिलिटी मेकओव्हर) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; }
    
    .stApp { background: #0d1117; color: #f0f6fc !important; }
    
    /* --- डाव्या बाजूच्या साईडबारचा जबरदस्त लुक --- */
    [data-testid="stSidebar"] {
        background-color: #070a0e !important; 
        border-right: 3px solid #FFD700 !important;
        padding: 20px 10px;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFD700 !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div {
        background-color: #161b22 !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        border: 2px solid #30363d !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3rem; display: block;
    }
    
    /* टॅबमधील मजकूर मोठा आणि चमकदार करण्यासाठी */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #161b22; padding: 8px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #21262d; border-radius: 6px;
        color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important;
    }
    .stTabs [aria-selected="true"] { background-color: #FFD700 !important; color: #0d1117 !important; }
    
    .glass-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    .footer-container { border-top: 1px solid #30363d; padding-top: 25px; margin-top: 50px; text-align: center; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

# --- ६. पहिली सुरक्षित भाषा निवड लोड करणे (ज्यामुळे एरर येणार नाही) ---
if "global_language_selector" in st.session_state:
    selected_lang_key = st.session_state["global_language_selector"]
else:
    selected_lang_key = "मराठी (Marathi) - महाराष्ट्र"

target_lang = languages_map[selected_lang_key]
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

# --- ७. डाव्या साईडबारचे सादरीकरण ---
selected_display_lang = st.sidebar.selectbox(
    current_ui["menu_lbl"],
    list(languages_map.keys()),
    index=list(languages_map.keys()).index(selected_lang_key),
    key="global_language_selector"
)

# पुनर्प्राप्ती (Re-evaluation) भाषा बदलल्यास
target_lang = languages_map[selected_display_lang]
current_ui = UI_LANG_MATRIX.get(target_lang, UI_LANG_MATRIX["English"])

# मुख्य ४ पर्याय (ज्यामुळे आता प्रत्येक क्लिक १००% काम करेल)
app_mode = st.sidebar.radio(
    current_ui["nav_lbl"], 
    [current_ui["dash_menu"], current_ui["sandbox_menu"], current_ui["doubt_menu"], current_ui["login_menu"]]
)

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

base_ai_instruction = f"""
You are the elite AI Engine of 'Abhyas Kranti' App, completely customized for {target_lang}.
1. Respond ONLY and strictly in '{target_lang}'.
2. Automatically adapt context, schemes, rules, and logic for the state mentioned in '{selected_display_lang}'.
"""

# ==========================================
# विभाग १: Dashboard
# ==========================================
if app_mode == current_ui["dash_menu"]:
    st.markdown('<span class="main-title">Abhyas Kranti National Portal</span>', unsafe_allow_html=True)
    st.markdown(f"#### {current_ui['dash_menu']}")
    st.markdown(f"**🌍 Active System Rules & Language Context:** `{selected_display_lang}`")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card"><h3>Dynamic Localization</h3><p>System automatically maps Central and State education rules synchronously upon language toggle.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><h3>IIT Patna Capstone</h3><p>Enterprise layout tailored for high-contrast accessibility in rural ecosystems.</p></div>', unsafe_allow_html=True)

# ==========================================
# विभाग २: ६-इन-१ AI सँडबॉक्स (आता पूर्णपणे गुजराती भाषेत चालेल!)
# ==========================================
elif app_mode == current_ui["sandbox_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["sandbox_menu"]}</span>', unsafe_allow_html=True)
    
    # टॅबची नावे डिक्शनरीमधून बदलतात, गुजराती निवडल्यास पूर्ण गुजराती होतील!
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(current_ui["tabs"])

    with tab1:
        st.markdown(f"### {current_ui['tabs'][0]}")
        user_query = st.text_input(current_ui["q1_lbl"], key="q1_sandbox")
        if st.button(current_ui["btn1_lbl"], key="btn1_sandbox"):
            with st.spinner("Processing..."):
                st.write(fetch_ai_response(user_query, base_ai_instruction + "Give detailed study answer in bullet points."))

    with tab2:
        st.markdown(f"### {current_ui['tabs'][1]}")
        exam_target = st.text_input(current_ui["q2_lbl"], "Board Exam", key="q2")
        hours = st.slider(current_ui["s2_lbl"], 1, 12, 5, key="s2")
        if st.button(current_ui["btn2_lbl"], key="btn2"):
            with st.spinner("Planning..."):
                st.write(fetch_ai_response(f"Exam: {exam_target}, Hours: {hours}", base_ai_instruction + "Create 7 day schedule."))

    with tab3:
        st.markdown(f"### {current_ui['tabs'][2]}")
        edu = st.selectbox(current_ui["sel3_lbl"], current_ui["edu_opts"], key="edu_lvl")
        inc = st.selectbox(current_ui["inc3_lbl"], current_ui["inc_opts"], key="inc_lvl")
        cat = st.text_input(current_ui["cat3_lbl"], "OBC", key="cat")
        if st.button(current_ui["btn3_lbl"], key="btn3"):
            with st.spinner("Searching..."):
                st.write(fetch_ai_response(f"Edu: {edu}, Income: {inc}, Cat: {cat}", base_ai_instruction + "Suggest 3 state-specific or global scholarships."))

    with tab4:
        st.markdown(f"### {current_ui['tabs'][3]}")
        tier = st.selectbox(current_ui["sel4_lbl"], current_ui["exam_tiers"], key="ex_lvl")
        ex_name = st.text_input(current_ui["txt4_lbl"], "PSC", key="ex_name")
        if st.button(current_ui["btn4_lbl"], key="btn4"):
            with st.spinner("Analyzing..."):
                st.write(fetch_ai_response(f"Tier: {tier}, Exam: {ex_name}", base_ai_instruction + "Give latest exam structure and 1 sample MCQ with answer."))

    with tab5:
        st.markdown(f"### {current_ui['tabs'][4]}")
        stream = st.selectbox(current_ui["sel5_lbl"], current_ui["streams"], key="stream")
        scope = st.radio(current_ui["rad5_lbl"], current_ui["scopes"], key="scope")
        interest = st.text_input(current_ui["txt5_lbl"], "Automation & Solar", key="interest")
        if st.button(current_ui["btn5_lbl"], key="btn5"):
            with st.spinner("Mapping..."):
                st.write(fetch_ai_response(f"Stream: {stream}, Scope: {scope}, Interest: {interest}", base_ai_instruction + "Provide 3 futuristic career roadmaps with official clickable markdown links [Website](URL)."))

    with tab6:
        st.markdown(f"### {current_ui['tabs'][5]}")
        st.success(f"✔️ Multilingual Synchronization Active for: {selected_display_lang}")

# ==========================================
# विभाग ३: स्वतंत्र शंका निरसन केंद्र (Doubt Solver)
# ==========================================
elif app_mode == current_ui["doubt_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["doubt_menu"]}</span>', unsafe_allow_html=True)
    st.markdown("---")
    user_query = st.text_input(current_ui["q1_lbl"], key="q1_direct")
    if st.button(current_ui["btn1_lbl"], key="btn1_direct"):
        with st.spinner("AI Mentor is thinking..."):
            st.write(fetch_ai_response(user_query, base_ai_instruction + "Give direct and clean solutions."))

# ==========================================
# विभाग ४: लॉगिन / प्रोफाईल (Login / Profile)
# ==========================================
elif app_mode == current_ui["login_menu"]:
    st.markdown(f'<span class="main-title">{current_ui["login_menu"]}</span>', unsafe_allow_html=True)
    st.markdown("---")
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
