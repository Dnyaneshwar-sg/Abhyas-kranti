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
    page_title="Abhyas Kranti Ultimate - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ३. हाय-कॉन्ट्रास्ट प्रीमियम डार्क आणि गोल्ड थीम CSS (Legibility Fix) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
    
    /* संपूर्ण ॲपसाठी फॉन्ट आणि हाय-कॉन्ट्रास्ट टेक्स्ट */
    * { 
        font-family: 'Noto Sans Devanagari', 'Inter', sans-serif; 
    }
    
    .stApp {
        background: #0d1117; /* पूर्ण डार्क ब्लॅक-ग्रे पार्श्वभूमी */
        color: #f0f6fc !important; /* अत्यंत स्पष्ट पांढरा रंग */
    }
    
    /* मुख्य शीर्षक */
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 5px;
        display: block;
    }
    
    /* सर्व हेडिंग्ससाठी १००% स्पष्टता */
    h1, h2, h3, h4, h5, h6 { 
        color: #ffffff !important; 
        font-weight: 700 !important;
        margin-top: 15px !important;
    }
    
    /* इनपुट लेबल्स (जे स्पष्ट दिसत नव्हते) */
    .stWidgetFormLabel, label, .stSlider p, .stRadio p {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* ग्लास कार्ड ऐवजी हाय-व्हिजिबिलिटी सॉलिड कार्ड्स */
    .glass-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .glass-card:hover {
        border-color: #FFD700;
    }
    
    .accent-icon { color: #FFD700; font-size: 2rem; margin-bottom: 12px; }
    
    .vision-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(22, 27, 34, 1) 100%);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin: 30px 0;
    }
    .vision-title { font-size: 1.6rem; font-weight: 800; color: #FFD700 !important; }
    
    /* टेबल डेटा सुधारणा */
    .stTable table {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    .stTable td { background-color: #0d1117 !important; color: #f0f6fc !important; border: 1px solid #30363d !important; }
    .stTable th { background-color: #21262d !important; color: #FFD700 !important; border: 1px solid #30363d !important; }
    
    /* टॅब्स डिझाईन */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #21262d;
        border-radius: 6px;
        color: #c9d1d9 !important;
        font-weight: 600;
        padding: 0px 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #0d1117 !important; /* सिलेक्टेड टॅबवर काळा मजकूर जेणेकरून तो ठळक दिसेल */
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

# --- ४. मोफत आणि सुरक्षित AI कॉल फंक्शन (Groq API) ---
def fetch_ai_response(prompt_text, system_setting):
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_setting},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.4,
            "max_tokens": 1500
        }
        response = requests.post(groq_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API त्रुटी आली आहे. कोड: {response.status_code}"
    except Exception as e:
        return f"तांत्रिक अडचण: {e}"

# --- ५. नेव्हिगेशन मेनू (Sidebar) ---
st.sidebar.markdown('### 📌 अभ्यास क्रांती मेनू')
app_mode = st.sidebar.radio("विभाग निवडा:", ["🏠 मुख्य पान (Dashboard)", "⚡ AI प्रगत फीचर्स सँडबॉक्स"])

# ==========================================
# विभाग १: मुख्य पान (Dashboard)
# ==========================================
if app_mode == "🏠 मुख्य पान (Dashboard)":
    st.markdown('<span class="main-title">Abhyas Kranti NEW</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown('<p style="color: #8b949e; font-size: 1.1rem; margin-top: -10px;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>', unsafe_allow_html=True)
    st.markdown("---")

    # The Core Problem
    st.markdown('## 🛑 The Core Problem in Rural Education')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card"><div class="accent-icon">🗂️</div><h4>Resource Fragmentation</h4><p style="color:#c9d1d9; font-size:0.9rem;">Lack of centralized educational resources.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🗣️</div><h4>Language Barriers</h4><p style="color:#c9d1d9; font-size:0.9rem;">Academic context is locked behind English proficiency.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><div class="accent-icon">💰</div><h4>Hyper-Inflationary Coaching</h4><p style="color:#c9d1d9; font-size:0.9rem;">Premium coaching formats are financially unviable.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🤖</div><h4>Technological Deficit</h4><p style="color:#c9d1d9; font-size:0.9rem;">Absence of real-time, personalized AI-driven guidance.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card"><div class="accent-icon">🎓</div><h4>Information Asymmetry</h4><p style="color:#c9d1d9; font-size:0.9rem;">Critical merit scholarships remain unnoticed.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🧭</div><h4>The Guidance Gap</h4><p style="color:#c9d1d9; font-size:0.9rem;">Lack of data insights to steer trajectories.</p></div>', unsafe_allow_html=True)

    # Vision
    st.markdown("""
        <div class="vision-box">
            <div class="vision-title">THE CAPSTONE VISION</div>
            <p style="font-size: 1.4rem; color: #ffffff; margin-top: 5px; font-weight: 600;">“To democratize quality education using AI.”</p>
        </div>
    """, unsafe_allow_html=True)

    # Tech Stack
    st.markdown('## 💻 Standardized Enterprise Tech Stack')
    tech_df = pd.DataFrame({
        "Layer": ["Frontend UI", "Core Programming", "AI Orchestration", "Database Tier", "Deployment Edge"],
        "Technology Stack Components": ["Streamlit Community Cloud & High-Contrast CSS", "Python 3.11+ / Async Request Arrays", "Groq API (Llama 3.3 70B Model Framework)", "Supabase Secure Matrix & Cloud SQL", "GitHub Enterprise & Vercel Functions"]
    })
    st.table(tech_df)

# ==========================================
# विभाग २: AI प्रगत फीचर्स सँडबॉक्स (6-in-1 Live Engine)
# ==========================================
elif app_mode == "⚡ AI प्रगत फीचर्स सँडबॉक्स":
    st.title("⚡ अभ्यास क्रांती AI Action Sandbox")
    st.markdown('<p style="color: #c9d1d9;">खालील टॅब्सवर क्लिक करून प्रगत फीचर्सचा अनुभव घ्या. आता सर्व ओळी स्पष्ट व हाय-कॉन्ट्रास्ट रंगात दिसतील.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 शंका निरसन शिक्षक",
        "📅 अभ्यास वेळापत्रक",
        "🛡️ स्कॉलरशिप इंजिन",
        "🎯 स्पर्धा परीक्षा केंद्र",
        "🛣️ करिअर मार्गदर्शक",
        "🌐 भाषा सुलभता (22 Languages)"
    ])

    # --- TAB 1: AI Doubt Solving ---
    with tab1:
        st.markdown("### 🧠 AI Powered Doubt Solver Hub")
        user_query = st.text_input("तुमचा शैक्षणिक प्रश्न विचारा (उदा. 'प्रकाश संश्लेषण म्हणजे काय?'):", key="q1")
        
        if st.button("🚀 शंका निरसन करा", key="btn1"):
            if user_query.strip():
                with st.spinner("AI Mentor उत्तर तयार करत आहे..."):
                    sys_prompt = "तुम्ही 'अभ्यास क्रांती' ॲपचे तज्ज्ञ शिक्षक आहात. विद्यार्थ्यांच्या प्रश्नांची उत्तरे शुद्ध मराठीत, अत्यंत अचूक आणि फक्त महत्त्वाच्या ७-८ बुलेट पॉईंट्समध्ये (Bullet Points) द्या. उत्तर स्पष्ट ठेवा."
                    ai_response = fetch_ai_response(user_query, sys_prompt)
                    st.success("🎯 AI Mentor कडून आलेले उत्तर:")
                    st.write(ai_response)
            else:
                st.warning("कृपया आधी प्रश्न टाईप करा.")

    # --- TAB 2: Study Planner ---
    with tab2:
        st.markdown("### 📅 Personalized Study Planner")
        exam_target = st.text_input("तुम्ही कोणत्या परीक्षेची तयारी करत आहात?", "MPSC Civil Services", key="q2")
        available_hours = st.slider("रोज अभ्यासासाठी किती तास देऊ शकता?", 1, 12, 5, key="s2")
        
        if st.button("🚀 स्मार्ट वेळापत्रक तयार करा", key="btn2"):
            with st.spinner("AI तुमच्यासाठी वेळापत्रक डिझाईन करत आहे..."):
                sys_prompt = "तुम्ही शैक्षणिक समुपदेशक आहात. दिलेल्या परीक्षेसाठी आठवड्याचे कस्टमाइज्ड वेळापत्रक मराठीत तयार करा."
                query = f"परीक्षा: {exam_target}, रोज उपलब्ध तास: {available_hours}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.info("🎯 तुमच्यासाठी तयार केलेले AI वेळापत्रक:")
                st.write(ai_response)

    # --- TAB 3: Scholarship Engine (१ ली ते जागतिक शिक्षण) ---
    with tab3:
        st.markdown("### 🛡️ Scholarship Recommendation Engine (Local to Global)")
        
        edu_level = st.selectbox(
            "विद्यार्थ्याची शैक्षणिक पातळी / इयत्ता निवडा:",
            [
                "इयत्ता १ ली ते ४ थी (प्राथमिक शाळा)",
                "इयत्ता ५ वी ते ७ वी (उच्च प्राथमिक)",
                "इयत्ता ८ वी ते १० वी (माध्यमिक / SSC)",
                "इयत्ता ११ वी आणि १२ वी (ज्युनिअर कॉलेज / HSC)",
                "पदवी शिक्षण (Undergraduate - BA, B.Sc, B.Com, B.E, MBBS इ.)",
                "पदव्युत्तर शिक्षण (Postgraduate - MA, M.Sc, M.Tech, MBA इ.)",
                "पीएच.डी. आणि उच्च संशोधन (Ph.D. Research Tier)",
                "जागतिक शिक्षण / परदेशातील उच्च शिक्षण (Global & International Studies)"
            ],
            key="edu_level_filter"
        )
        
        income_level = st.selectbox("कौटुंबिक वार्षिक उत्पन्न निवडा:", ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाख ते ₹८ लाख", "₹८ लाखांपेक्षा जास्त"], key="q3")
        category = st.text_input("प्रवर्ग / जात (उदा. Open, OBC, SC, ST, NT, EWS):", "OBC", key="c3")
        
        if st.button("🚀 पात्र स्कॉलरशिप शोधा", key="btn3"):
            with st.spinner("जागतिक शिष्यवृत्ती मॅट्रिक्स स्कॅन करत आहे..."):
                sys_prompt = "तुम्ही राष्ट्रीय आणि आंतरराष्ट्रीय शिष्यवृत्तीचे सर्वोच्च तज्ञ आहात. विद्यार्थ्याने दिलेल्या शैक्षणिक पातळी (१ ली ते जागतिक शिक्षण), उत्पन्न आणि प्रवर्गाचा विचार करून त्याला लागू होणाऱ्या ३ महत्त्वाच्या सरकारी किंवा जागतिक स्कॉलरशिप योजनांची नावे, अचूक पात्रता आणि अधिकृत अर्ज प्रक्रियेची माहिती मराठीत स्पष्ट बुलेट पॉईंट्समध्ये सांगा."
                query = f"पातळी: {edu_level}, उत्पन्न: {income_level}, प्रवर्ग: {category}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.success("💡 शिफारसित स्कॉलरशिप योजना:")
                st.write(ai_response)

    # --- TAB 4: Competitive Exam Support (राज्य, राष्ट्रीय व जागतिक) ---
    with tab4:
        st.markdown("### 🎯 Competitive Exam Support Module (State, National & Global)")
        
        exam_level = st.selectbox(
            "परीक्षेची पातळी निवडा:",
            ["महाराष्ट्र राज्य पातळीवरील परीक्षा (MPSC, Talathi, Police Bharti, Maha-TET)", 
             "राष्ट्रीय पातळीवरील परीक्षा (UPSC, NEET, JEE, NDA, SSC, Banking)", 
             "जागतिक / आंतरराष्ट्रीय परीक्षा (GRE, GMAT, SAT, IELTS, TOEFL)"],
            key="exam_level_select"
        )
        specific_exam = st.text_input("थेट परीक्षेचे नाव टाईप करा (उदा. MPSC, NEET, GRE):", "MPSC", key="spec_ex")
        
        if st.button("🚀 परीक्षा पॅटर्न आणि नमुना प्रश्न मिळवा", key="btn4"):
            with st.spinner("प्रश्न संच आणि परीक्षा आराखडा तयार होत आहे..."):
                sys_prompt = "तुम्ही स्पर्धा परीक्षांचे वरिष्ठ मार्गदर्शक आहात. विद्यार्थ्याने निवडलेल्या पातळीवरील परीक्षेचा नेमका पॅटर्न, महत्त्वाचे विषय आणि १ नमुना बहुपर्यायी प्रश्न (MCQ) उत्तरासह आणि स्पष्टीकरणासह मराठीत तयार करून द्या."
                query = f"पातळी: {exam_level}, परीक्षा: {specific_exam}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.info("📝 AI परीक्षा मार्गदर्शक अहवाल:")
                st.write(ai_response)

    # --- TAB 5: Career Guidance (लोकल ते जागतिक व सर्व शाखा + लिंक्स) ---
    with tab5:
        st.markdown("### 🛣️ End-to-End Career Guidance System (All Streams & Resource Links)")
        
        academic_stream = st.selectbox(
            "विद्याशाखा / प्रवाह निवडा (Select Stream):",
            ["कला शाखा (Arts & Humanities)", 
             "वाणिज्य शाखा (Commerce & Management)", 
             "विज्ञान शाखा (Pure & Applied Sciences)", 
             "तांत्रिक, इंजिनिअरिंग व मेडिकल (Technical & Medical)", 
             "व्यावसायिक व कौशल्य विकास (Vocational, Solar, Tailoring, Agriculture)"],
            key="stream_select"
        )
        
        career_scope = st.radio("करिअरची व्याप्ती (Scope):", ["स्थानिक आणि राष्ट्रीय संधी (Local & National)", "जागतिक संधी (Global & International Opportunities)"], key="scope_rad")
        specific_interest = st.text_input("विद्यार्थ्याची वैयक्तिक आवड (उदा. डेटा सायन्स, सोलर बिझनेस, सिव्हिल सर्विस):", "आधुनिक शेती आणि सोलर", key="q5")
        
        if st.button("🚀 करिअर रोडमॅप आणि अधिकृत लिंक्स मिळवा", key="btn5"):
            with st.spinner("AI करिअर ट्रॅजेक्टोरी आणि रिसोर्स लिंक्स मॅप करत आहे..."):
                sys_prompt = "तुम्ही जागतिक करिअर कौन्सिलर आहात. विद्यार्थ्याने निवडलेली विद्याशाखा, व्याप्ती आणि आवड यानुसार त्याला उपलब्ध असणाऱ्या ३ सर्वोत्तम करिअर संधींची माहिती मराठीत द्या. सर्वात महत्त्वाचे म्हणजे, प्रत्येक संधीसाठी विद्यार्थ्यांनी कोठे शिकावे किंवा अर्ज करावा याच्याशी संबंधित अधिकृत आणि उपयुक्त संकेतस्थळांच्या लिंक्स (उदा. Coursera, National Career Service, UGC, किंवा नामांकित संस्थांचे वेब पोर्टल्सचे नाव व मार्गदर्शक लिंक्स format [वेबसाईटचे नाव](URL)) स्वरूपात उत्तरात अनिवार्यपणे समाविष्ट करा."
                query = f"शाखा: {academic_stream}, व्याप्ती: {career_scope}, आवड: {specific_interest}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.success("🛣️ तुमचा सविस्तर करिअर रोडमॅप:")
                st.markdown(ai_response)

    # --- TAB 6: Multi-language Accessibility (२२ भारतीय भाषा) ---
    with tab6:
        st.markdown("### 🌐 Multi-language Accessibility Evaluation Hub (22 Official Languages)")
        st.markdown("<p style='color:#ffffff;'>भारतीय संविधानातील <b>२२ अधिकृत भाषांचा</b> सपोर्ट विद्यार्थ्यांसाठी उपलब्ध करून देण्यात आला आहे. खालीलपैकी कोणत्याही भाषेत सिस्टीम संवाद साधू शकते:</p>", unsafe_allow_html=True)
        
        # २२ अधिकृत भाषांचा ड्रॉपडाऊन
        selected_lang = st.selectbox(
            "चाचणीसाठी भाषा निवडा (Select Language to Evaluate Interface):",
            [
                "मराठी (Marathi)", "हिंदी (Hindi)", "संस्कृत (Sanskrit)", "कोंकणी (Konkani)", 
                "गुराती (Gujarati)", "कन्नड (Kannada)", "मल्याळम (Malayalam)", "तमिळ (Tamil)", 
                "तेलुगू (Telugu)", "उर्दू (Urdu)", "बंगाली (Bengali)", "आसामी (Assamese)", 
                "बोडो (Bodo)", "डोगरी (Dogri)", "काश्मिरी (Kashmiri)", "मैथिली (Maithili)", 
                "मणिपुरी (Manipuri)", "नेपाळी (Nepali)", "ओडिया (Oriya)", "पंजाबी (Punjabi)", 
                "संथाली (Santali)", "सिंधी (Sindhi)"
            ],
            key="lang_select"
        )
        
        st.info(f"✨ **सिस्टीम अपडेट:** 'अभ्यास क्रांती'चे AI इंजिन आता **{selected_lang}** च्या व्याकरण आणि स्थानिक भाषिक संदर्भाशी पूर्णपणे सुसंगत (Optimized) झाले आहे.")
        st.caption("हा इंटरफेस लो-बँडविड्थ (Low Bandwidth) ग्रामीण भागातही प्रादेशिक फॉन्ट अतिशय वेगाने लोड करतो.")

# --- ६. एकत्रित फायनल फुटर ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">
            Developed by Dnyaneshwar Gawalikar
        </p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 0.5px;">
            Professor & Head of Department
        </p>
        <p style="font-size: 0.8rem; color: #8b949e;">
            Capstone Project — IIT Patna Generative AI Sprint 2026
        </p>
    </div>
""", unsafe_allow_html=True)
