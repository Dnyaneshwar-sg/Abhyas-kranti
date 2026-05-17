import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="Abhyas Kranti NEW",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* HIDE STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* MAIN BG */
.stApp{
    background: linear-gradient(135deg,#050816,#0b1023,#101935);
    color:white;
    font-family:sans-serif;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:#0a0f1f;
    border-right:1px solid rgba(255,255,255,0.08);
}

/* HERO */
.hero-box{
    padding:45px;
    border-radius:30px;
    background:linear-gradient(
        135deg,
        rgba(255,193,7,0.15),
        rgba(255,255,255,0.03)
    );
    border:1px solid rgba(255,255,255,0.08);
    margin-top:20px;
    margin-bottom:30px;
}

/* TITLES */
.main-title{
    font-size:68px;
    font-weight:900;
    line-height:1.1;
    color:white;
}

.yellow{
    color:#FFC107;
}

.subtitle{
    font-size:22px;
    color:#FFD54F;
    margin-top:15px;
    font-weight:700;
}

.desc{
    font-size:20px;
    margin-top:20px;
    color:#d9d9d9;
}

/* BUTTONS */
.btn{
    padding:14px 28px;
    border-radius:16px;
    background:#FFC107;
    color:black;
    font-weight:700;
    text-align:center;
    margin-top:15px;
}

/* STATS */
.stat-box{
    padding:30px;
    border-radius:22px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    margin-top:20px;
}

.stat-number{
    font-size:48px;
    font-weight:900;
}

.stat-label{
    font-size:18px;
}

/* CARDS */
.card{
    padding:30px;
    border-radius:24px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    margin-top:25px;
}

.card-title{
    font-size:28px;
    font-weight:800;
    margin-bottom:15px;
}

.card-text{
    font-size:18px;
    line-height:1.8;
    color:#e0e0e0;
}

/* SECTION TITLE */
.section-title{
    font-size:42px;
    font-weight:900;
    margin-top:40px;
    margin-bottom:10px;
}

/* FOOTER */
.footer-box{
    margin-top:70px;
    padding:35px;
    border-radius:24px;

    background:linear-gradient(
        135deg,
        rgba(255,193,7,0.08),
        rgba(255,255,255,0.03)
    );

    border:1px solid rgba(255,255,255,0.08);

    text-align:center;
}

.footer-title{
    color:#FFD54F;
    font-size:42px;
    font-weight:900;
}

.footer-name{
    font-size:36px;
    font-weight:800;
    margin-top:20px;
}

.footer-sub{
    font-size:22px;
    color:#dddddd;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.markdown("""
# 🚀 Abhyas Kranti NEW

### AI Powered Indian Education Platform
""")

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero-box">

<div style="color:#FFC107;font-weight:800;">
🚀 A SOCIAL INITIATIVE BY DR. DNYANESHWAR GAWALIKAR
</div>

<br>

<div class="main-title">
Empowering Students from
<br>
<span class="yellow">Class 1 to Global Careers</span>
</div>

<div class="subtitle">
क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची!
</div>

<div class="desc">
AI Powered Indian Education Platform for School Students,
NEET/JEE Aspirants, UPSC/MPSC Students, Scholarship Seekers,
Research Scholars and Global Education Aspirants.
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# BUTTONS
# =========================

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown('<div class="btn">📚 Explore Sections</div>',unsafe_allow_html=True)

with c2:
    st.markdown('<div class="btn">🧠 Take Free Quiz</div>',unsafe_allow_html=True)

with c3:
    st.markdown('<div class="btn">🎥 Watch Video Lessons</div>',unsafe_allow_html=True)

# =========================
# STATS
# =========================

s1,s2,s3,s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class="stat-box">
    <div class="stat-number">10,000+</div>
    <div class="stat-label">Students</div>
    </div>
    """,unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="stat-box">
    <div class="stat-number">50+</div>
    <div class="stat-label">Exams</div>
    </div>
    """,unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="stat-box">
    <div class="stat-number">500+</div>
    <div class="stat-label">Scholarships</div>
    </div>
    """,unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="stat-box">
    <div class="stat-number">3</div>
    <div class="stat-label">Languages</div>
    </div>
    """,unsafe_allow_html=True)

# =========================
# PROBLEM STATEMENT
# =========================

st.markdown('<div class="section-title">❗ Problem Statement</div>',unsafe_allow_html=True)

st.markdown("""
<div class="card">
<div class="card-title">Educational Challenges in Rural India</div>

<div class="card-text">

• Lack of centralized educational resources<br>
• Expensive coaching ecosystem<br>
• Scholarship awareness issues<br>
• Career guidance gap<br>
• Language barriers<br>
• Lack of AI-powered support systems<br>
• Difficulty accessing government opportunities

</div>
</div>
""",unsafe_allow_html=True)

# =========================
# SOLUTION
# =========================

st.markdown('<div class="section-title">💡 Our Solution</div>',unsafe_allow_html=True)

a,b,c = st.columns(3)

with a:
    st.markdown("""
    <div class="card">
    <div class="card-title">🧠 AI Mentor</div>
    <div class="card-text">
    AI powered educational guidance, doubt solving and career support.
    </div>
    </div>
    """,unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card">
    <div class="card-title">🗓 Smart Planner</div>
    <div class="card-text">
    Personalized timetable and preparation strategies for exams.
    </div>
    </div>
    """,unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="card">
    <div class="card-title">🎓 Scholarship Engine</div>
    <div class="card-text">
    Scholarship discovery from Class 1 to PhD level.
    </div>
    </div>
    """,unsafe_allow_html=True)

# =========================
# TECH STACK
# =========================

st.markdown('<div class="section-title">🛠 Technology Stack</div>',unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text">

✅ Frontend → Streamlit<br>
✅ Backend → Python<br>
✅ AI → Google Gemini API<br>
✅ Database → SQLite<br>
✅ Charts → Plotly<br>
✅ Deployment → Streamlit Cloud

</div>

</div>
""",unsafe_allow_html=True)

# =========================
# IMPACT
# =========================

st.markdown('<div class="section-title">🌍 Impact</div>',unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text">

✅ Designed for Rural India<br>
✅ Multi-language Education Access<br>
✅ Free Government Resources<br>
✅ Competitive Exam Support<br>
✅ AI Powered Learning Assistance<br>
✅ Centralized Education Ecosystem

</div>

</div>
""",unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer-box">

<div class="footer-title">
“शिका, स्पर्धा करा, यशस्वी व्हा — हेच आमचं ध्येय!”
</div>

<div class="footer-name">
Dnyaneshwar Gawalikar
</div>

<div class="footer-sub">
Capstone Project — IIT Patna
</div>
st.markdown('<div class="section-title">🎯 Objectives</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text">


✅ Centralized education ecosystem<br>
✅ AI-powered student guidance<br>
✅ Scholarship awareness<br>
✅ Competitive exam support<br>
✅ Rural India accessibility<br>
✅ Multi-language learning support

</div>

</div>
""", unsafe_allow_html=True)


