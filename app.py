import streamlit as st
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #121620 0%, #08090c 100%);
        color: #e2e8f0;
    }

    /* Global Title Styling Override */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        line-height: 1.2;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: transform 0.3s ease, border-color 0.3s ease;
        margin-bottom: 20px;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 215, 0, 0.4);
    }

    /* Feature Icon/Badge Style */
    .accent-icon {
        color: #FFD700;
        font-size: 1.8rem;
        margin-bottom: 10px;
    }

    /* Premium Vision Callout Box */
    .vision-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.02) 100%);
        border-left: 5px solid #FFD700;
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        margin: 40px 0;
    }

    .vision-title {
        font-size: 2rem;
        font-weight: 700;
        color: #FFD700 !important;
        letter-spacing: 1px;
    }

    /* Workflow Architecture Flow */
    .arch-step {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: 600;
    }

    .arch-arrow {
        text-align: center;
        font-size: 2rem;
        color: #FFD700;
        line-height: 2.5;
    }

    /* Buttons Styling Customizations */
    .div-cta-container {
        display: flex;
        gap: 15px;
        margin-top: 25px;
        margin-bottom: 40px;
    }

    .cta-button {
        padding: 10px 24px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        transition: all 0.3s ease;
    }

    .cta-primary {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #08090c !important;
    }

    .cta-primary:hover {
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        transform: scale(1.03);
    }

    .cta-secondary {
        background: transparent;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .cta-secondary:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #FFD700;
    }

    /* Table Styling for Dark Theme */
    .dataframe {
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    
    th {
        background-color: rgba(255, 215, 0, 0.1) !important;
        color: #FFD700 !important;
        font-weight: 600 !important;
    }

    /* Footer Section */
    .footer-container {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 30px;
        margin-top: 60px;
        text-align: center;
        color: #a0aec0;
        font-size: 0.95rem;
    }

    /* Custom spacing */
    .section-spacing {
        padding-top: 50px;
        padding-bottom: 20px;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. HERO SECTION
# ==========================================
st.markdown('<p class="gradient-text">Abhyas Kranti NEW</p>', unsafe_allow_html=True)
st.markdown('### AI Powered Educational Ecosystem for Rural India')
st.markdown('<p style="color: #a0aec0; font-size: 1.1rem; margin-top: -10px;">Capstone Project — IIT Patna Generative AI Sprint 2026</p>', unsafe_allow_html=True)

# Modern Interactive CTA Section using Streamlit columns & anchor styling
st.markdown("""
    <div class="div-cta-container">
        <a class="cta-button cta-primary" href="#features-section">Explore Features</a>
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
st.markdown('Despite technological advancements, rural ecosystems face systemic bottlenecks that restrict student growth:')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🗂️</div>
            <h4>Resource Fragmentation</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Lack of centralized educational resources, forcing students to rely on scattered, unverified study materials.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🗣️</div>
            <h4>Language Barriers</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">High-quality cutting-edge academic context is often locked behind English proficiency, sidelining vernacular students.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">💰</div>
            <h4>Hyper-Inflationary Coaching</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Premium competitive coaching formats are commercially gated and financially unviable for rural households.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🤖</div>
            <h4>Technological Deficit</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Absence of real-time, personalized AI-driven guidance systems optimized for low-bandwidth zones.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🎓</div>
            <h4>Information Asymmetry</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Critical state merit scholarships and corporate financial assistance programs remain completely unnoticed.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <div class="accent-icon">🧭</div>
            <h4>The Guidance Gap</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">A complete lack of structured data insights to steer students toward modern alternative career trajectories.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. VISION SECTION
# ==========================================
st.markdown("""
    <div class="vision-box">
        <div class="vision-title">THE CAPSTONE VISION</div>
        <p style="font-size: 1.5rem; color: #ffffff; margin-top: 10px; font-weight: 300;">
            “To democratize quality education using AI.”
        </p>
        <p style="color: #a0aec0; font-size: 0.95rem; max-width: 700px; margin: 0 auto;">
            Bridging the socio-economic and geographical divides by deploying context-aware, low-latency infrastructure built specifically for the needs of upcoming leaders in rural communities.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. OBJECTIVES SECTION
# ==========================================
st.markdown('## 🎯 Core Project Objectives')
obj_col1, obj_col2, obj_col3, obj_col4, obj_col5 = st.columns(5)

with obj_col1:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 15px;"><div class="accent-icon">🧠</div><h5>AI Mentor</h5><p style="font-size:0.85rem; color:#cbd5e1;">24/7 on-demand localized tutoring</p></div>', unsafe_allow_html=True)
with obj_col2:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 15px;"><div class="accent-icon">📅</div><h5>Smart Planner</h5><p style="font-size:0.85rem; color:#cbd5e1;">Hyper-tailored dynamic learning timetables</p></div>', unsafe_allow_html=True)
with obj_col3:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 15px;"><div class="accent-icon">🛡️</div><h5>Scholarship</h5><p style="font-size:0.85rem; color:#cbd5e1;">Predictive financial discovery engines</p></div>', unsafe_allow_html=True)
with obj_col4:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 15px;"><div class="accent-icon">🛣️</div><h5>Career Guide</h5><p style="font-size:0.85rem; color:#cbd5e1;">Mapping alternate modern trajectories</p></div>', unsafe_allow_html=True)
with obj_col5:
    st.markdown('<div class="glass-card" style="text-align: center; padding: 15px;"><div class="accent-icon">🌐</div><h5>Multi-Lingual</h5><p style="font-size:0.85rem; color:#cbd5e1;">Deep local vernacular adaptations</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 5. SOLUTION ARCHITECTURE
# ==========================================
st.markdown('<div id="architecture-section" class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 🏗️ End-to-End Solution Architecture')
st.markdown('The system utilizes a modern decouple workflow that safely handles inputs, processing pipelines, and personalized generation tracking:')

a_col1, a_arr1, a_col2, a_arr2, a_col3, a_arr3, a_col4 = st.columns([2, 0.5, 2, 0.5, 2, 0.5, 2])

with a_col1:
    st.markdown('<div class="arch-step">🧑‍🎓 Rural Student<br><span style="font-size:0.8rem; color:#a0aec0; font-weight:400;">Web Interface Inputs</span></div>', unsafe_allow_html=True)
with a_arr1:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col2:
    st.markdown('<div class="arch-step" style="border-color:#FFD700;">⚙️ GenAI Orchestrator<br><span style="font-size:0.8rem; color:#FFD700; font-weight:400;">LLM Frameworks</span></div>', unsafe_allow_html=True)
with a_arr2:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col3:
    st.markdown('<div class="arch-step">📊 Personalized Core<br><span style="font-size:0.8rem; color:#a0aec0; font-weight:400;">Context Tuning Matrices</span></div>', unsafe_allow_html=True)
with a_arr3:
    st.markdown('<div class="arch-arrow">→</div>', unsafe_allow_html=True)
with a_col4:
    st.markdown('<div class="arch-step" style="background:rgba(255,215,0,0.05);">🏆 Continuous Success<br><span style="font-size:0.8rem; color:#FFD700; font-weight:400;">Exams / Scholarships</span></div>', unsafe_allow_html=True)

# ==========================================
# 6. TECHNOLOGY STACK
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 💻 Standardized Enterprise Tech Stack')

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown('🗣️ **Frontend UI Framework**')
    st.markdown('* Streamlit (Rapid App Prototyping)\n* Advanced Custom CSS / Glassmorphism UI Components')
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
    st.markdown('* Razorpay Webhooks (For micro-grants access)')

with tech_col4:
    st.markdown('🚀 **Deployment Vectors**')
    st.markdown('* GitHub Enterprise Repositories\n* Vercel Cloud Native Edge Functions')

st.markdown("---")

# ==========================================
# 7. CAPSTONE TIMELINE
# ==========================================
st.markdown('## 📅 Capstone Execution Timeline')
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
st.markdown('<div id="features-section"></div>', unsafe_allow_html=True)
st.markdown('<div id="demo-section" class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## ⚡ Live Mock Capstone Feature Sandbox')
st.markdown('Select an AI sub-engine option to evaluate systemic mock data processing configurations:')

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

if "1." in feature_tab:
    st.markdown("### 🧠 AI Powered Doubt Solver Hub")
    st.info("Simulated Environment Engine running real-time context maps.")
    user_query = st.text_input("Enter a complex question (e.g., 'Explain Photosynthesis'):", "Explain Laws of Motion")
    if st.button("Initialize Generative Response Inference"):
        st.success(f"**AI Response Ecosystem for query '{user_query}':** This system processes the requested concept step-by-step using local vernacular examples and simplistic physical real-world analogs tailored to maximize retention profiles without heavy jargon.")

elif "2." in feature_tab:
    st.markdown("### 📅 Personalized Localized Study Planner")
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

imp_col1, imp_col2 = st.columns(2)

with imp_col1:
    st.markdown("""
        <div class="glass-card">
            <h4>💡 High Socio-Economic Upskilling</h4>
            <p style="color: #cbd5e1;">By making complex engineering, medical, and public service entrance methodologies accessible directly at zero cost barrier locations, structural wealth disparity impacts are negated over performance cycles.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h4>🤝 Scholarship Discovery Optimization</h4>
            <p style="color: #cbd5e1;">Converts hidden financial channels into actionable assets. Ensures deserving talent lines get immediate state-backed educational support without agent exploitation networks.</p>
        </div>
    """, unsafe_allow_html=True)

with imp_col2:
    st.markdown("""
        <div class="glass-card">
            <h4>📉 Radical Coaching Overhead Reductions</h4>
            <p style="color: #cbd5e1;">Removes the logistical imperative for students to migrate to premium urban tier centers by creating top-tier cognitive AI mentors directly in localized village nodes.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h4>🪐 Democratization of Advanced LLM Technologies</h4>
            <p style="color: #cbd5e1;">Synthesizes complex algorithmic frameworks into simple accessible interfaces, turning bleeding-edge technology into functional civic utilities for the segments that need it most.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. FUTURE SCOPE
# ==========================================
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('## 🚀 Future Roadmap & Scaling Vectors')

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
        <p style="font-size: 1.1rem; color: #ffffff; font-weight: 600; margin-bottom: 5px;">
            Developed by Ved (Dnyaneshwar Gawalikar)
        </p>
        <p style="color: #FFD700; font-weight: 500; margin-bottom: 20px;">
            Professor & Head of Department
        </p>
        <p style="font-size: 0.85rem; color: #718096;">
            Capstone Project — IIT Patna Generative AI Sprint 2026
        </p>
    </div>
""", unsafe_allow_html=True)
