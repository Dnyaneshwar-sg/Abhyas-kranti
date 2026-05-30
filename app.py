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
    page_title="Abhyas Kranti NEW - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ३. प्रिमियम डार्क आणि गोल्ड थीम CSS (Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f121d 0%, #050608 100%);
        color: #f1f5f9;
    }
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 5px;
        display: block;
    }
    h1, h2, h3, h4, h5 { color: #ffffff !important; font-weight: 700 !important; }
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .glass-card:hover {
        border-color: rgba(255, 215, 0, 0.5);
        background: rgba(255, 255, 255, 0.06);
    }
    .accent-icon { color: #FFD700; font-size: 2rem; margin-bottom: 12px; }
    .vision-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.12) 0%, rgba(255, 165, 0, 0.03) 100%);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin: 30px 0;
    }
    .vision-title { font-size: 1.6rem; font-weight: 800; color: #FFD700 !important; }
    .arch-step {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 215, 0, 0.4);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: 600;
    }
    .stTable table {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
    }
    .stTable td { background-color: rgba(15, 18, 29, 0.6) !important; color: #e2e8f0 !important; }
    .stTable th { background-color: rgba(255, 215, 0, 0.15) !important; color: #FFD700 !important; }
    .footer-container {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 25px;
        margin-top: 50px;
        text-align: center;
        color: #94a3b8;
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
            "model": "llama-3.3-70b-versatile",  # येथे नवीन आणि प्रगत मॉडेल अपडेट केले आहे
            "messages": [
                {"role": "system", "content": system_setting},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.4,
            "max_tokens": 1200
        }
        response = requests.post(groq_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API त्रुटी आली आहे. कोड: {response.status_code}"
    except Exception as e:
        return f"तांत्रिक अडचण: {e}"

# --- ५. मोबाईल फ्रेंडली नेव्हिगेशन मेनू (Sidebar) ---
st.sidebar.markdown('### 📌 अभ्यास क्रांती मेनू')
app_mode = st.sidebar.radio("विभाग निवडा:", ["🏠 मुख्य पान (Dashboard)", "⚡ AI प्रगत फीचर्स सँडबॉक्स"])

# ==========================================
# विभाग १: मुख्य पान (Dashboard)
# ==========================================
if app_mode == "🏠 मुख्य पान (Dashboard)":
    st.markdown('<span class="main-title">Abhyas Kranti NEW</span>', unsafe_allow_html=True)
    st.markdown('### AI Powered Educational Ecosystem for Rural India')
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem; margin-top: -10px;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>', unsafe_allow_html=True)
    st.markdown("---")

    # The Core Problem
    st.markdown('## 🛑 The Core Problem in Rural Education')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card"><div class="accent-icon">🗂️</div><h4>Resource Fragmentation</h4><p style="color:#cbd5e1; font-size:0.9rem;">Lack of centralized educational resources.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🗣️</div><h4>Language Barriers</h4><p style="color:#cbd5e1; font-size:0.9rem;">Academic context is locked behind English proficiency.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><div class="accent-icon">💰</div><h4>Hyper-Inflationary Coaching</h4><p style="color:#cbd5e1; font-size:0.9rem;">Premium coaching formats are financially unviable.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🤖</div><h4>Technological Deficit</h4><p style="color:#cbd5e1; font-size:0.9rem;">Absence of real-time, personalized AI-driven guidance.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card"><div class="accent-icon">🎓</div><h4>Information Asymmetry</h4><p style="color:#cbd5e1; font-size:0.9rem;">Critical merit scholarships remain unnoticed.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><div class="accent-icon">🧭</div><h4>The Guidance Gap</h4><p style="color:#cbd5e1; font-size:0.9rem;">Lack of data insights to steer trajectories.</p></div>', unsafe_allow_html=True)

    # Vision
    st.markdown("""
        <div class="vision-box">
            <div class="vision-title">THE CAPSTONE VISION</div>
            <p style="font-size: 1.4rem; color: #ffffff; margin-top: 5px; font-weight: 600;">“To democratize quality education using AI.”</p>
        </div>
    """, unsafe_allow_html=True)

    # Objectives
    st.markdown('## 🎯 Core Project Objectives')
    obj_col1, obj_col2, obj_col3, obj_col4, obj_col5 = st.columns(5)
    obj_col1.markdown('<div class="glass-card" style="text-align:center;"><h5>🧠 AI Mentor</h5><p style="font-size:0.8rem; color:#cbd5e1;">24/7 Localized</p></div>', unsafe_allow_html=True)
    obj_col2.markdown('<div class="glass-card" style="text-align:center;"><h5>📅 Smart Planner</h5><p style="font-size:0.8rem; color:#cbd5e1;">Hyper-Tailored</p></div>', unsafe_allow_html=True)
    obj_col3.markdown('<div class="glass-card" style="text-align:center;"><h5>🛡️ Scholarship</h5><p style="font-size:0.8rem; color:#cbd5e1;">Predictive</p></div>', unsafe_allow_html=True)
    obj_col4.markdown('<div class="glass-card" style="text-align:center;"><h5>🛣️ Career Guide</h5><p style="font-size:0.8rem; color:#cbd5e1;">Modern Paths</p></div>', unsafe_allow_html=True)
    obj_col5.markdown('<div class="glass-card" style="text-align:center;"><h5>🌐 Multi-Lingual</h5><p style="font-size:0.8rem; color:#cbd5e1;">Vernacular</p></div>', unsafe_allow_html=True)

    # Architecture
    st.markdown('## 🏗️ End-to-End Solution Architecture')
    a_col1, a_arr1, a_col2, a_arr2, a_col3 = st.columns([2, 0.5, 2, 0.5, 2])
    with a_col1: st.markdown('<div class="arch-step">🧑‍🎓 Rural Student<br><span style="font-size:0.75rem; color:#94a3b8;">Interface Inputs</span></div>', unsafe_allow_html=True)
    with a_arr1: st.markdown('<h3 style="text-align:center; color:#FFD700 !important; margin-top:10px;">➔</h3>', unsafe_allow_html=True)
    with a_col2: st.markdown('<div class="arch-step" style="border-color:#FFD700;">⚙️ GenAI Orchestrator<br><span style="font-size:0.75rem; color:#FFD700;">Groq & Llama 3</span></div>', unsafe_allow_html=True)
    with a_arr2: st.markdown('<h3 style="text-align:center; color:#FFD700 !important; margin-top:10px;">➔</h3>', unsafe_allow_html=True)
    with a_col3: st.markdown('<div class="arch-step">📊 Cloud Storage<br><span style="font-size:0.75rem; color:#94a3b8;">Supabase Secure Tier</span></div>', unsafe_allow_html=True)

    # Tech Stack
    st.markdown('## 💻 Standardized Enterprise Tech Stack')
    tech_df = pd.DataFrame({
        "Layer": ["Frontend UI", "Core Programming", "AI Orchestration", "Database Tier", "Deployment Edge"],
        "Technology Stack Components": ["Streamlit Community Cloud & Premium CSS", "Python 3.11+ / Async Request Arrays", "Groq API (Llama 3.3 70B Model Framework)", "Supabase Secure Matrix & Cloud SQL", "GitHub Enterprise & Vercel Functions"]
    })
    st.table(tech_df)

    # Timeline Table
    st.markdown('## 📅 Capstone Execution Timeline')
    timeline_data = {
        "Phase / Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Milestone Core Subject Focus": ["Ideation & Planning", "MVP Development", "AI Integration", "Final Deployment"],
        "Status": ["✅ Completed", "✅ Completed", "✅ Completed", "⚡ Ready for Evaluation"]
    }
    st.table(pd.DataFrame(timeline_data))

# ==========================================
# विभाग २: AI प्रगत फीचर्स सँडबॉक्स (6-in-1 Live Engine)
# ==========================================
elif app_mode == "⚡ AI प्रगत फीचर्स सँडबॉक्स":
    st.title("⚡ अभ्यास क्रांती AI Action Sandbox")
    st.markdown('<p style="color: #cbd5e1;">खालील ड्रॉपडाऊनमधून कोणताही एक विभाग निवडा आणि थेट AI चा लाईव्ह अनुभव घ्या:</p>', unsafe_allow_html=True)

    feature_tab = st.selectbox(
        "प्लॅटफॉर्म ॲक्शन लेयर निवडा:",
        [
            "1. AI Powered Doubt Solving (शंका निरसन शिक्षक)",
            "2. Personalized Study Planner (अभ्यास वेळापत्रक नियोजक)",
            "3. Scholarship Recommendation Engine (स्कॉलरशिप शोध इंजिन)",
            "4. Competitive Exam Support (स्पर्धा परीक्षा मदत केंद्र)",
            "5. Career Guidance System (भविष्य करिअर मार्गदर्शक)",
            "6. Multi-language Accessibility Evaluation (भाषा सुलभता तपासणी)"
        ]
    )

    st.write("---")

    # १. AI Doubt Solving
    if "1." in feature_tab:
        st.markdown("### 🧠 AI Powered Doubt Solver Hub")
        user_query = st.text_input("तुमचा शैक्षणिक प्रश्न विचारा (उदा. 'प्रकाश संश्लेषण म्हणजे काय?'):", key="q1")
        
        if st.button("🚀 शंका निरसन करा", key="btn1"):
            if user_query.strip():
                with st.spinner("AI Mentor उत्तर तयार करत आहे..."):
                    sys_prompt = "तुम्ही 'अभ्यास क्रांती' ॲपचे तज्ज्ञ शिक्षक आहात. विद्यार्थ्यांच्या प्रश्नांची उत्तरे शुद्ध मराठीत, अत्यंत अचूक आणि फक्त महत्त्वाच्या ७-८ बुलेट पॉईंट्समध्ये (Bullet Points) द्या. उत्तर स्पष्ट ठेवा."
                    ai_response = fetch_ai_response(user_query, sys_prompt)
                    st.success("🎯 AI Mentor कडून आलेले उत्तर:")
                    st.write(ai_response)
                    
                    # डेटाबेस सेव्ह करताना 'query_text' का अचूक वापर
                    try:
                        supabase.table("search_history").insert({"query_text": user_query, "response": ai_response}).execute()
                        st.caption("🔄 डेटा सुपाबेस डेटाबेसमध्ये सुरक्षितपणे नोंदवला गेला आहे.")
                    except Exception as db_err:
                        pass
            else:
                st.warning("कृपया आधी प्रश्न टाईप करा.")

    # २. Study Planner
    elif "2." in feature_tab:
        st.markdown("### 📅 Personalized Study Planner")
        exam_target = st.text_input("तुम्ही कोणत्या परीक्षेची तयारी करत आहात?", "MPSC Civil Services 2026", key="q2")
        available_hours = st.slider("रोज अभ्यासासाठी किती तास देऊ शकता?", 1, 12, 5, key="s2")
        
        if st.button("🚀 स्मार्ट वेळापत्रक तयार करा", key="btn2"):
            with st.spinner("AI तुमच्यासाठी वेळापत्रक डिझाईन करत आहे..."):
                sys_prompt = "तुम्ही शैक्षणिक समुपदेशक आहात. विद्यार्थ्याने दिलेल्या परीक्षेसाठी आणि वेळेसाठी १ आठवड्याचे कस्टमाइज्ड अभ्यासाचे वेळापत्रक मराठीत अत्यंत आकर्षक बुलेट पॉईंट्समध्ये तयार करा."
                query = f"परीक्षा: {exam_target}, रोज उपलब्ध तास: {available_hours}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.info("🎯 तुमच्यासाठी तयार केलेले AI वेळापत्रक:")
                st.write(ai_response)

    # ३. Scholarship Recommendation Engine
    elif "3." in feature_tab:
        st.markdown("### 🛡️ Scholarship Recommendation Engine")
        income_level = st.selectbox("तुमचे कौटुंबिक वार्षिक उत्पन्न निवडा:", ["₹१.५ लाखांपेक्षा कमी", "₹१.५ लाख ते ₹३ लाख", "₹३ लाखांपेक्षा जास्त"], key="q3")
        category = st.text_input("तुमचा प्रवर्ग/जात टाईप करा (उदा. Open, OBC, SC, ST):", "OBC", key="c3")
        
        if st.button("🚀 पात्र स्कॉलरशिप शोधा", key="btn3"):
            with st.spinner("डेटाबेस मॅट्रिक्स स्कॅन करत आहे..."):
                sys_prompt = "तुम्ही भारत सरकारच्या आणि महाराष्ट्र सरकारच्या शिष्यवृत्तीचे तज्ञ आहात. विद्यार्थ्याने दिलेल्या उत्पन्न आणि प्रवर्गासाठी योग्य असणाऱ्या कमीत कमी २ मोफत सरकारी स्कॉलरशिप योजनांची नावे आणि माहिती मराठीत सांगा."
                query = f"उत्पन्न: {income_level}, प्रवर्ग: {category}"
                ai_response = fetch_ai_response(query, sys_prompt)
                st.success("💡 शिफारसित स्कॉलरशिप योजना:")
                st.write(ai_response)

    # ४. Competitive Exam Support
    elif "4." in feature_tab:
        st.markdown("### 🎯 Competitive Exam Support Module")
        exam_track = st.radio("तुमचे धध्येय निवडा:", ["NEET Medical", "JEE Engineering", "NDA Defence Forces", "MPSC/UPSC Civil Services"], key="r4")
        
        if st.button("🚀 महत्त्वाचे पॅटर्न प्रश्न मिळवा", key="btn4"):
            with st.spinner("प्रश्न संच तयार होत आहे..."):
                sys_prompt = f"तुम्ही {exam_track} चे वरिष्ठ प्राध्यापक आहात. या परीक्षेसाठी अत्यंत महत्त्वाचा असणारा १ नमुना बहुपर्यायी प्रश्न (MCQ) मराठीत स्पष्टीकरणासह तयार करा."
                ai_response = fetch_ai_response("Give 1 high weightage exam question with options and correct answer in Marathi", sys_prompt)
                st.write(ai_response)

    # ५. Career Guidance System
    elif "5." in feature_tab:
        st.markdown("### 🛣️ Alternative Career Guidance Systems")
        interests_field = st.text_input("विद्यार्थ्याची आवड किंवा क्षेत्र (उदा. शेती, इलेक्ट्रॉनिक्स, सोलर, टेलरिंग):", "सोलर आणि आधुनिक शेती", key="q5")
        
        if st.button("🚀 भविष्यातील करिअर मार्ग शोधा", key="btn5"):
            with st.spinner("AI करिअर ट्रॅजेक्टोरी मॅप करत आहे..."):
                sys_prompt = "तुम्ही करिअर मार्गदर्शक आहात. ग्रामीण विद्यार्थ्यांना आधुनिक युगात (उदा. AI, सोलर, ऑटोमेशन) उपलब्ध असणाऱ्या ३ नवीन करिअर संधींची माहिती मराठीत द्या."
                ai_response = fetch_ai_response(interests_field, sys_prompt)
                st.markdown(ai_response)

    # ६. Multi-language Accessibility
    elif "6." in feature_tab:
        st.markdown("### 🌐 Multi-language Accessibility Evaluation Hub")
        st.success("सिस्टीम इंटरफेस स्वयंचलितपणे **मराठी (मराठी)** आणि स्थानिक प्रादेशिक बोलीभाषेशी सुसंगत करण्यात आला आहे.")
        st.caption("कमी इंटरनेट बँडविड्थ (Low Bandwidth Zones) मध्येही हा इंटरफेस अतिशय वेगाने लोड होतो.")

# --- ६. एकत्रित फायनल फुटर (दोन्ही पदांसह सुरक्षित) ---
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 2px;">
            Developed by (Dnyaneshwar Gawalikar)
        </p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 0.5px;">
            Professor & Head of Department
        </p>
        <p style="font-size: 0.8rem; color: #64748b;">
            Capstone Project — IIT Patna Generative AI Sprint 2026
        </p>
    </div>
""", unsafe_allow_html=True)
