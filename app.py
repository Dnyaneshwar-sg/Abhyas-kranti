import streamlit as st
from supabase import create_client, Client

# १. Secrets मधून सुपाबेसच्या चाव्या (Keys) लोड करणे
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# २. सुपाबेस क्लायंट कॉन्फिगर करणे
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
import pandas as pd

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Abhyas Kranti NEW - IIT Patna Capstone",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Premium CSS for Dark Theme, Glassmorphism, and Gold Accents
st.markdown("""
    <style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f121d 0%, #050608 100%);
        color: #f1f5f9;
    }

    /* Fix for Big Heading and visibility issues */
    .main-title {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.8rem;
        margin-bottom: 5px;
        line-height: 1.2;
        display: block;
    }

    /* Global Title Styling Override */
    h1, h2, h3, h4, h5 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 215, 0, 0.5);
        background: rgba(255, 255, 255, 0.06);
    }

    /* Feature Icon/Badge Style */
    .accent-icon {
        color: #FFD700;
        font-size: 2rem;
        margin-bottom: 15px;
    }

    /* Premium Vision Callout Box */
    .vision-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.12) 0%, rgba(255, 165, 0, 0.03) 100%);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 35px;
        text-align: center;
        margin: 40px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .vision-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFD700 !important;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    /* Workflow Architecture Flow */
    .arch-step {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 215, 0, 0.4);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .arch-arrow {
        text-align: center;
        font-size: 2rem;
        color: #FFD700;
        line-height: 2.2;
    }

    /* Buttons Styling Customizations */
    .div-cta-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 25px;
        margin-bottom: 40px;
    }

    .cta-button {
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }

    .cta-primary {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #050608 !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }

    .cta-primary:hover {
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
        transform: scale(1.05);
    }

    .cta-secondary {
        background: rgba(255, 255, 255, 0.03);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .cta-secondary:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #FFD700;
        transform: translateY(-2px);
    }

    /* CRITICAL FIX: Table Styling for Visibility */
    .stTable table {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stTable td {
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        padding: 15px !important;
        background-color: rgba(15, 18, 29, 0.6) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .stTable th {
        background-color: rgba(255, 215, 0, 0.15) !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }

    /* Footer Section */
    .footer-container {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 35px;
        margin-top: 70px;
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .section-spacing {
        padding-top: 40px;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. HERO SECTION
# ==========================================
st.markdown('<span class="main-title">Abhyas Kranti NEW</span>', unsafe_allow_html=True)
st.markdown('### AI Powered Educational Ecosystem for Rural India')
st.markdown('<p style="color: #94a3b8; font-size: 1.15rem; margin-top: -10px;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>', unsafe_allow_html=True)

# Modern Interactive CTA Buttons
st.markdown("""
    <div class="div-cta-container">
        <a class="cta-button cta-primary" href="#explore-features">Explore Features</a>
        <a class="cta-button cta-secondary" href="#architecture-section">View Architecture</a>
        <a class="cta-button cta-secondary" href="#demo-section">Interactive Demo</a>
        <a class="cta-button cta-secondary" href="https://github.com" target="_blank">🔗 GitHub Repository</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 2. PROBLEM STATEMENT
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 🛑 The Core Problem in Rural Education')
st.markdown('<p style="color: #cbd5e1; font-size: 1.05rem; margin-bottom: 25px;">Despite technological advancements, rural ecosystems face systemic bottlenecks that restrict student growth:</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🗂️</div>
            <h4>Resource Fragmentation</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">Lack of centralized educational resources, forcing students to rely on scattered, unverified study materials.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🗣️</div>
            <h4>Language Barriers</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">High-quality cutting-edge academic context is often locked behind English proficiency, sidelining vernacular students.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">💰</div>
            <h4>Hyper-Inflationary Coaching</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">Premium competitive coaching formats are commercially gated and financially unviable for rural households.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🤖</div>
            <h4>Technological Deficit</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">Absence of real-time, personalized AI-driven guidance systems optimized for low-bandwidth zones.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🎓</div>
            <h4>Information Asymmetry</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">Critical state merit scholarships and corporate financial assistance programs remain completely unnoticed.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🧭</div>
            <h4>The Guidance Gap</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">A complete lack of structured data insights to steer students toward modern alternative career trajectories.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. VISION SECTION
# ==========================================
st.markdown("""
    <div class="vision-box">
        <div class="vision-title">THE CAPSTONE VISION</div>
        <p style="font-size: 1.6rem; color: #ffffff; margin-top: 10px; font-weight: 600; letter-spacing: 0.5px;">
            “To democratize quality education using AI.”
        </p>
        <p style="color: #94a3b8; font-size: 1rem; max-width: 800px; margin: 15px auto 0 auto; line-height: 1.6;">
            Bridging the socio-economic and geographical divides by deploying context-aware, low-latency infrastructure built specifically for the needs of upcoming leaders in rural communities.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. OBJECTIVES SECTION
# ==========================================
st.markdown('<div id="explore-features"></div>', unsafe_allow_html=True)
st.markdown('## 🎯 Core Project Objectives')
st.write("")
obj_col1, obj_col2, obj_col3, obj_col4, obj_col5 = st.columns(5)

with obj_col1:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 20px;"><div class="accent-icon">🧠</div><h5>AI Mentor</h5><p style="font-size:0.88rem; color:#cbd5e1; margin-top:10px;">24/7 on-demand localized tutoring</p></div>', unsafe_allow_html=True)
with obj_col2:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 20px;"><div class="accent-icon">📅</div><h5>Smart Planner</h5><p style="font-size:0.88rem; color:#cbd5e1; margin-top:10px;">Hyper-tailored dynamic timetables</p></div>', unsafe_allow_html=True)
with obj_col3:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 20px;"><div class="accent-icon">🛡️</div><h5>Scholarship</h5><p style="font-size:0.88rem; color:#cbd5e1; margin-top:10px;">Predictive financial discovery</p></div>', unsafe_allow_html=True)
with obj_col4:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 20px;"><div class="accent-icon">🛣️</div><h5>Career Guide</h5><p style="font-size:0.88rem; color:#cbd5e1; margin-top:10px;">Mapping alternate modern paths</p></div>', unsafe_allow_html=True)
with obj_col5:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 20px;"><div class="accent-icon">🌐</div><h5>Multi-Lingual</h5><p style="font-size:0.88rem; color:#cbd5e1; margin-top:10px;">Deep local vernacular adaptations</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 5. SOLUTION ARCHITECTURE
# ==========================================
st.markdown('<div id="architecture-section" class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 🏗️ End-to-End Solution Architecture')
st.markdown('<p style="color: #cbd5e1; margin-bottom: 25px;">The system utilizes a modern decoupled workflow that safely handles inputs, processing pipelines, and personalized generation tracking:</p>', unsafe_allow_html=True)

a_col1, a_arr1, a_col2, a_arr2, a_col3, a_arr3, a_col4 = st.columns([2, 0.4, 2, 0.4, 2, 0.4, 2])

with a_col1:
    st.markdown('<div class="arch-step">🧑‍🎓 Rural Student<br><span style="font-size:0.8rem; color:#94a3b8; font-weight:400; display:block; margin-top:5px;">Web Interface Inputs</span></div>', unsafe_allow_html=True)
with a_arr1:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col2:
    st.markdown('<div class="arch-step" style="border-color:#FFD700; background: rgba(255,215,0,0.02);">⚙️ GenAI Orchestrator<br><span style="font-size:0.8rem; color:#FFD700; font-weight:400; display:block; margin-top:5px;">LLM Frameworks</span></div>', unsafe_allow_html=True)
with a_arr2:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col3:
    st.markdown('<div class="arch-step">📊 Personalized Core<br><span style="font-size:0.8rem; color:#94a3b8; font-weight:400; display:block; margin-top:5px;">Context Tuning Matrices</span></div>', unsafe_allow_html=True)
with a_arr3:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col4:
    st.markdown('<div class="arch-step" style="background:rgba(255,215,0,0.05); border-style: solid;">🏆 Continuous Success<br><span style="font-size:0.8rem; color:#FFD700; font-weight:400; display:block; margin-top:5px;">Exams / Scholarships</span></div>', unsafe_allow_html=True)

# ==========================================
# 6. TECHNOLOGY STACK
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 💻 Standardized Enterprise Tech Stack')
st.write("")

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown('🗣️ **Frontend UI Framework**')
    st.markdown('* Streamlit (Rapid App Prototyping)\n* Advanced Custom CSS / Glassmorphism')
    st.markdown('🐍 **Core Logic Programming**')
    st.markdown('* Python 3.11+\n* Async Operations Pipelines')

with tech_col2:
    st.markdown('🧠 **Core AI Orchestration**')
    st.markdown('* Google Gemini API Framework\n* Custom Prompt Injection Layers')
    st.markdown('📦 **Data Storage Tier**')
    st.markdown('* SQLite (Rapid Edge Caching Data Model)')

with tech_col3:
    st.markdown('☁️ **Cloud Database Layer**')
    st.markdown('* Supabase Security Matrix Integration')
    st.markdown('💳 **Gateway Adaptations**')
    st.markdown('* Razorpay Webhooks (Micro-grants access)')

with tech_col4:
    st.markdown('🚀 **Deployment Vectors**')
    st.markdown('* GitHub Enterprise Repositories\n* Vercel Cloud Native Edge Functions')

st.markdown("---")

# ==========================================
# 7. CAPSTONE TIMELINE
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 📅 Capstone Execution Timeline')
st.write("")

timeline_data = {
    "Phase / Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "Milestone Core Subject Focus": ["Ideation & Planning", "MVP Development", "AI Integration", "Final Deployment"],
    "Technical Key Deliverables": [
        "Architecture formulation, requirements engineering, validation criteria baseline mapping.",
        "Database provisioning via Supabase, basic web engine application components generation.",
        "Gemini LLM pipeline API tuning, dynamic context vector injections validation testing.",
        "UI fine tuning, platform resilience testing, staging checks, production launch on Streamlit cloud."
    ],
    "Status": ["✅ Completed", "✅ Completed", "✅ Completed", "⚡ Ready for Evaluation"]
}
timeline_df = pd.DataFrame(timeline_data)
st.table(timeline_df)

# ==========================================
# 8. LIVE FUNCTIONAL FEATURES (INTERACTIVE DEMO)
# ==========================================
st.markdown('<div id="demo-section" class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## ⚡ Live Mock Capstone Feature Sandbox')
st.markdown('<p style="color: #cbd5e1; margin-bottom: 20px;">Select an AI sub-engine option to evaluate systemic mock data processing configurations:</p>', unsafe_allow_html=True)

feature_tab = st.selectbox(
    "Choose Platform Action Layer:",
    [
        "1. AI Powered Doubt Solving",
        "2. Personalized Study Planner",
        "3. Scholarship Recommendation Engine",
        "4. Competitive Exam Support",
        "5. Career Guidance System",
        "6. Multi-language Accessibility Evaluation"
    ]
)

st.write("")
if "1." in feature_tab:
    st.markdown("### 🧠 AI Powered Doubt Solver Hub (Powered by Groq)")
    st.info("Simulated Environment Engine running real-time context maps.")
    
    user_query = st.text_input("Enter a complex question (e.g., 'Explain Photosynthesis'):", key="doubt_solver_input")
    
    if st.button("Initialize Generative Response Inference"):
        if user_query.strip() == "":
            st.warning("कृपया आधी तुमचा प्रश्न टाईप करा!")
     else:
        with st.spinner("Groq AI कडून उत्तर आणत आहे..."):
            try:
                # Groq API की आणि युआरएल सेट करणे
                groq_api_key = st.secrets["GROQ_API_KEY"]
                groq_url = "https://api.groq.com/openai/v1/chat/completions"

                headers = {
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                }

                # सिस्टीम प्रॉम्ट - उत्तरे अचूक आणि बुलेट पॉईंट्समध्ये मिळवण्यासाठी
                messages = [
                    {
                        "role": "system", 
                        "content": "तुम्ही 'अभ्यास क्रांती' ॲपचे तज्ज्ञ आणि मार्गदर्शक शिक्षक आहात. विद्यार्थ्यांच्या प्रश्नांची उत्तरे शुद्ध मराठीत, अत्यंत अचूक आणि फक्त महत्त्वाच्या ७-८ बुलेट पॉईंट्समध्ये (Bullet Points) द्या. कोणत्याही शब्दाची किंवा वाक्याची वारंवार पुनरावृत्ती करू नका. उत्तर संक्षिप्त, सुंदर आणि स्पष्ट ठेवा."
                    },
                    {
                        "role": "user", 
                        "content": user_query
                    }
                ]

                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 800
                }

                # Groq कडून रिस्पॉन्स मिळवणे
                import requests
                import json

                response = requests.post(groq_url, headers=headers, data=json.dumps(payload))

                if response.status_code == 200:
                        result = response.json()
                        ai_output = result['choices'][0]['message']['content']
                        
                        # स्क्रीनवर उत्तर दाखवणे
                        st.success(ai_output)
                        
                        # २. सुपाबेस डेटाबेसमध्ये एंट्री सेव्ह करणे
                        try:
                            url = st.secrets["SUPABASE_URL"]
                            key = st.secrets["SUPABASE_KEY"]
                            supabase_client = create_client(url, key)
                            
                            doubt_data = {
                                "student_id": "STU_RURAL_01",
                                "query_text": user_query,
                                "ai_response": ai_output,
                                "status": "completed"
                            }
                            
                            supabase_client.table("doubt_logs").insert(doubt_data).execute()
                            st.caption("🔄 डेटा सुपाबेस डेटाबेसमध्ये सुरक्षितपणे नोंदवला गेला आहे.")
                            
                        except Exception as e_supabase:
                            st.error(f"सुपाबेस डेटाबेस एरर: {e_supabase}")
                    else:
                        st.error(f"Groq API एरर (कोड {response.status_code}): {response.text}")
                        
                except Exception as e_groq:
                    st.error(f"सिस्टम एरर: {e_groq}")
    exam_target = st.text_input("Target Examination Track:", "MPSC Civil Services 2026")
    available_hours = st.slider("Daily Available Study Windows (Hours):", 1, 8, 4)
    if st.button("Generate Optimized Study Blueprint"):
        st.code(f"// Abhyas Kranti Generated Timeline Schedule Matrix\n- Focus Subject Area: Core State Track syllabus mapping\n- Daily Commitment Threshold: {available_hours} Hours Structured Blocks\n- Revision Ratio Target: 25% of timeline allocation\n- Automated Progression Evaluations: Alternate Sunday Mock Windows", language="markdown")

elif "3." in feature_tab:
    st.markdown("### 🛡️ Scholarship Opportunity Recommendation Engine")
    income_level = st.selectbox("Annual Household Income Bracket Estimation:", ["Below ₹1,500,000", "₹1.5L to ₹3L", "Above ₹3L"])
    if st.button("Query Matching Scholarship Matrices"):
        if income_level == "Below ₹1,500,000":
            st.markdown("""
                * **Recommendation 1:** Post-Matric State Merit Scholarship (Covers 100% Tuition Fees)
                * **Recommendation 2:** National Means-cum-Merit Assistance Program Alignment
            """)
        else:
            st.markdown("* **Recommendation 1:** State Centralized Merit High-Performance Track Allotments")

elif "4." in feature_tab:
    st.markdown("### 🎯 Competitive Exam Support Module")
    exam_track = st.radio("Choose Target Academic Stream Assessment:", ["NEET Medical", "JEE Engineering", "NDA Defence Forces", "MPSC/UPSC Civil Services"])
    if st.button("Deploy Target Question Parameters"):
        st.write(f"Loading latest standardized AI generated problem arrays for tracking **{exam_track}** matrix patterns. High weightage evaluation maps are now queued.")

elif "5." in feature_tab:
    st.markdown("### 🛣️ Alternative Career Guidance Systems")
    interests_field = st.text_input("Input Core Student Interest Triggers:", "Agricultural Automation and Solar Grid Maintenance")
    if st.button("Execute Strategic Career Trajectory Mapping"):
        st.markdown(f"🚀 **Modern Career Pathways Detected for '{interests_field}':**\n1. Agro-Solar Operations Manager\n2. Rural Micro-Grid Technical Entrepreneur\n3. Precision Farming Automation Technician")

elif "6." in feature_tab:
    st.markdown("### 🌐 Multi-language Accessibility Evaluation Hub")
    lang_selection = st.selectbox("Target Regional Localization Pipeline:", ["Marathi (मराठी)", "Hindi (हिन्दी)", "Vernacular Context Adaptations"])
    st.write(f"System core localized translation interfaces automatically mapped to **{lang_selection}** configurations with low-latency compression layers.")

st.markdown("---")

# ==========================================
# 9. IMPACT SECTION
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 📈 Project Impact Matrix (Rural India Target Outcomes)')
st.write("")

imp_col1, imp_col2 = st.columns(2)

with imp_col1:
    st.markdown("""
        <div class="glass-card">
            <h4>💡 High Socio-Economic Upskilling</h4>
            <p style="color: #cbd5e1; line-height: 1.6;">By making complex engineering, medical, and public service entrance methodologies accessible directly at zero cost barrier locations, structural wealth disparity impacts are negated over performance cycles.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h4>🤝 Scholarship Discovery Optimization</h4>
            <p style="color: #cbd5e1; line-height: 1.6;">Converts hidden financial channels into actionable assets. Ensures deserving talent lines get immediate state-backed educational support without agent exploitation networks.</p>
        </div>
    """, unsafe_allow_html=True)

with imp_col2:
    st.markdown("""
        <div class="glass-card">
            <h4>📉 Radical Coaching Overhead Reductions</h4>
            <p style="color: #cbd5e1; line-height: 1.6;">Removes the logistical imperative for students to migrate to premium urban tier centers by creating top-tier cognitive AI mentors directly in localized village nodes.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h4>🪐 Democratization of Advanced LLM Technologies</h4>
            <p style="color: #cbd5e1; line-height: 1.6;">Synthesizes complex algorithmic frameworks into simple accessible interfaces, turning bleeding-edge technology into functional civic utilities for the segments that need it most.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. FUTURE SCOPE
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 🚀 Future Roadmap & Scaling Vectors')
st.write("")

f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    st.markdown("#### 📱 Native Android Deployments")
    st.markdown("Optimizing model quantization levels to allow local model caching layers to function smoothly on lightweight, sub-$100 smartphone chipsets under offline contexts.")
    st.markdown("#### 🎙️ Voice-to-Voice AI Layer")
    st.markdown("Integrating conversational voice assistants to allow low-literacy segments or younger students to naturally query tasks using simple native speech patterns.")

with f_col2:
    st.markdown("#### 🗣️ Extended Hyper-Local Dialects")
    st.markdown("Going beyond standard regional profiles to integrate local village colloquialisms, maximizing educational comprehension metrics.")
    st.markdown("#### 🎭 Generative Mock Interactive Panels")
    st.markdown("Deploying advanced audio-visual AI avatars that replicate live panel interview environments to train students for elite level competitive checks.")

with f_col3:
    st.markdown("#### 🏛️ Governance Infrastructure Integrations")
    st.markdown("Connecting system parameters directly to local Gram Panchayat digital dashboards to systematically announce educational updates in real time.")

# ==========================================
# 11. PUBLIC POST SECTION
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('### 📢 Capstone Public Engagement')
st.info("🔗 **Project Publication Baseline:** Shared via institutional tracks under tracking parameters: **#IITPatnaCapstone**")

# ==========================================
# 12. DEPLOYMENT SECTION
# ==========================================
st.markdown('### 🚀 Deployment Architecture Status')
st.markdown("""
* **Version Control Hub:** Hosted via GitHub Enterprise secure staging networks.
* **Production Processing Web Tier:** Anchored and compiled on Streamlit Cloud clusters.
* **Edge Routing Pipeline Integration:** Configured using Vercel serverless functions infrastructure.
""")

# ==========================================
# 13. FINAL FOOTER
# ==========================================
st.markdown("""
    <div class="footer-container">
        <p style="font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-bottom: 5px;">
            Developed by  (Dnyaneshwar Gawalikar)
        </p>
        <p style="color: #FFD700; font-weight: 600; margin-bottom: 20px; font-size: 0.95rem; letter-spacing: 0.5px;">
            Professor & Head of Department
        </p>
        <p style="font-size: 0.85rem; color: #64748b;">
            Capstone Project — IIT Patna Generative AI Sprint 2026
        </p>
    </div>
""", unsafe_allow_html=True)
