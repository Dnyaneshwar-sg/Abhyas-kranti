import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

import plotly.express as px
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Abhyas Kranti NEW",
    page_icon="",
    layout="wide"
)# ==============================
# ABHYAS KRANTI NEW
# PREMIUM CAPSTONE UI SECTION
# PASTE BELOW st.set_page_config()
# ==============================

st.markdown("""
<style>

/* -----------------------------
GLOBAL
----------------------------- */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(255,193,7,0.12), transparent 25%),
        linear-gradient(135deg,#050816,#0d132b,#10172f);
    color: white;
}

/* -----------------------------
SIDEBAR
----------------------------- */

section[data-testid="stSidebar"] {
    background: rgba(8,12,25,0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* -----------------------------
HERO
----------------------------- */

.hero-box {
    padding: 70px;
    border-radius: 32px;

    background:
        radial-gradient(circle at top right,
        rgba(255,193,7,0.18),
        transparent 28%),
        linear-gradient(
        145deg,
        rgba(255,255,255,0.05),
        rgba(255,255,255,0.02)
    );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.45);

    margin-bottom: 40px;
}

.hero-badge {
    display: inline-block;

    padding: 10px 20px;

    border-radius: 999px;

    border: 1px solid rgba(255,193,7,0.4);

    background: rgba(255,193,7,0.08);

    color: #ffc107;

    font-size: 14px;

    font-weight: 800;

    margin-bottom: 25px;
}

.hero-title {
    font-size: 72px;
    line-height: 1.1;
    font-weight: 900;
    margin-bottom: 20px;
}

.highlight {
    color: #ffc107;
}

.hero-subtitle {
    font-size: 30px;
    color: #ffd54f;
    font-weight: 700;
    margin-bottom: 20px;
}

.hero-description {
    font-size: 20px;
    color: rgba(255,255,255,0.8);
    line-height: 1.8;
    max-width: 1000px;
}

/* -----------------------------
BUTTONS
----------------------------- */

.stButton > button {
    background: linear-gradient(
        90deg,
        #ffc107,
        #ff9800
    );

    color: black !important;

    border: none;

    border-radius: 16px;

    padding: 14px 26px;

    font-size: 16px;

    font-weight: 800;

    transition: 0.3s ease;

    box-shadow:
        0 8px 25px rgba(255,193,7,0.25);
}

.stButton > button:hover {
    transform: translateY(-3px);
}

/* -----------------------------
SEARCH
----------------------------- */

.stTextInput input {
    background: rgba(255,255,255,0.06) !important;

    border-radius: 16px !important;

    border: 1px solid rgba(255,255,255,0.1) !important;

    color: white !important;

    height: 55px !important;
}

/* -----------------------------
CARDS
----------------------------- */

.card {
    background:
        linear-gradient(
        145deg,
        rgba(255,255,255,0.04),
        rgba(255,255,255,0.02)
    );

    border-radius: 24px;

    padding: 30px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 8px 30px rgba(0,0,0,0.25);

    transition: 0.3s ease;

    height: 100%;
}

.card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,193,7,0.4);
}

.card-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 15px;
}

.card-text {
    color: rgba(255,255,255,0.75);
    line-height: 1.7;
    font-size: 16px;
}

/* -----------------------------
STATS
----------------------------- */

.stat-card {
    background:
        linear-gradient(
        145deg,
        rgba(255,255,255,0.04),
        rgba(255,255,255,0.02)
    );

    border-radius: 24px;

    padding: 30px;

    text-align: center;

    border: 1px solid rgba(255,255,255,0.08);
}

.stat-number {
    font-size: 54px;
    font-weight: 900;
    color: white;
}

.stat-label {
    color: rgba(255,255,255,0.7);
    font-size: 18px;
}

/* -----------------------------
SECTION TITLE
----------------------------- */

.section-title {
    font-size: 42px;
    font-weight: 900;
    margin-top: 50px;
    margin-bottom: 25px;
}

/* -----------------------------
FOOTER
----------------------------- */

.footer-box {
    margin-top: 60px;

    background:
        linear-gradient(
        145deg,
        rgba(255,193,7,0.08),
        rgba(255,255,255,0.02)
    );

    border-radius: 24px;

    padding: 35px;

    text-align: center;

    border: 1px solid rgba(255,255,255,0.08);
}

.footer-text {
    font-size: 24px;
    color: #ffd54f;
    font-weight: 800;
}

/* -----------------------------
HIDE STREAMLIT
----------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================

st.markdown("""
<div class="hero-box">

<div class="hero-badge">
 A SOCIAL INITIATIVE BY DR. DNYANESHWAR GAWALIKAR
</div>

<div class="hero-title">
Empowering Students from
<br>
<span class="highlight">
Class 1 to Global Careers
</span>
</div>

<div class="hero-subtitle">
क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची!
</div>

<div class="hero-description">
AI Powered Indian Education Platform for
School Students, NEET/JEE Aspirants,
UPSC/MPSC Students, Scholarship Seekers,
Research Scholars and Global Education Aspirants.
</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# SEARCH
# ==============================

search = st.text_input(
    "Search",
    placeholder=" Search exams, scholarships, books, careers...",
    key="main_search_box"
)

# ==============================
# BUTTONS
# ==============================

c1, c2, c3 = st.columns(3)

with c1:
    st.button(" Explore Sections")

with c2:
    st.button(" Take Free Quiz")

with c3:
    st.button(" Watch Video Lessons")

# ==============================
# STATS
# ==============================

st.markdown("<br>", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">10,000+</div>
        <div class="stat-label">Students</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">50+</div>
        <div class="stat-label">Exams</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">500+</div>
        <div class="stat-label">Scholarships</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">Languages</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# PROBLEM STATEMENT
# ==============================

st.markdown(
    '<div class="section-title"> Problem Statement</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<div class="card-title">
Educational Challenges in Rural India
</div>

<div class="card-text">

• Lack of centralized educational resources  
• Expensive coaching ecosystem  
• Scholarship awareness issues  
• Career guidance gap  
• Language barriers  
• Lack of AI-powered support systems  
• Difficulty accessing government opportunities  

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# SOLUTION
# ==============================

st.markdown(
    '<div class="section-title"> Our Solution</div>',
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("""
    <div class="card">
        <div class="card-title"> AI Mentor</div>
        <div class="card-text">
        AI powered educational guidance,
        doubt solving and career support.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="card">
        <div class="card-title"> Smart Planner</div>
        <div class="card-text">
        Personalized timetable and
        preparation strategies for exams.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div class="card">
        <div class="card-title"> Scholarship Engine</div>
        <div class="card-text">
        Scholarship discovery from
        Class 1 to PhD level.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# FEATURES
# ==============================

st.markdown(
    '<div class="section-title"> Quick Access</div>',
    unsafe_allow_html=True
)
# ==============================
# FINAL CAPSTONE POLISH
# ABHYAS KRANTI NEW
# IIT PATNA CAPSTONE VERSION
# ==============================

# PASTE THIS BELOW YOUR CSS SECTION

# ==============================
# PREMIUM SIDEBAR
# ==============================

st.sidebar.markdown("""
<div style="
padding:20px;
border-radius:20px;
background:linear-gradient(
145deg,
rgba(255,193,7,0.12),
rgba(255,255,255,0.03)
);
border:1px solid rgba(255,255,255,0.08);
margin-bottom:20px;
text-align:center;
">

<h1 style="
font-size:28px;
margin-bottom:10px;
">

</h1>

<h2 style="
color:white;
margin-bottom:10px;
">
Abhyas Kranti NEW
</h2>

<p style="
color:rgba(255,255,255,0.7);
font-size:14px;
">
AI Powered Indian Education Platform
</p>

</div>
""", unsafe_allow_html=True)

# ==============================
# WHY THIS MATTERS
# ==============================

st.markdown("""
<div class="section-title">
 Why This Matters
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text" style="
font-size:22px;
line-height:2;
font-weight:600;
text-align:center;
">

India's rural students deserve
AI-powered educational equality.

<br><br>

Every student should have access to
guidance, scholarships, AI mentorship,
competitive exam preparation and
global educational opportunities —
regardless of financial background.

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# LIVE AI SECTION
# ==============================

st.markdown("""
<div class="section-title">
 Live AI Mentor Demo
</div>
""", unsafe_allow_html=True)

user_question = st.text_input(
    "Ask AI Mentor",
    placeholder="Ask anything about exams, careers, scholarships..."
)

if st.button(" Generate AI Answer"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is thinking..."):

            try:

                model = genai.GenerativeModel(
                    "models/gemini-1.5-flash"
                )

                response = model.generate_content(
                    user_question
                )

                st.success(response.text)

            except Exception as e:

                st.error(
                    f"AI Error: {str(e)}"
                )

# ==============================
# ANALYTICS SECTION
# ==============================

st.markdown("""
<div class="section-title">
 Student Analytics Dashboard
</div>
""", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    progress_data = pd.DataFrame({
        "Subject": [
            "Physics",
            "Chemistry",
            "Biology",
            "Maths"
        ],
        "Completion": [
            72,
            65,
            88,
            54
        ]
    })

    fig = px.bar(
        progress_data,
        x="Subject",
        y="Completion",
        title="Subject Completion %",
        text="Completion"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart_col2:

    study_data = pd.DataFrame({
        "Day": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],
        "Hours": [
            4,
            5,
            6,
            3,
            7,
            8,
            6
        ]
    })

    fig2 = px.line(
        study_data,
        x="Day",
        y="Hours",
        title="Weekly Study Hours",
        markers=True
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==============================
# EXAM ECOSYSTEM
# ==============================

st.markdown("""
<div class="section-title">
 Complete Exam Ecosystem
</div>
""", unsafe_allow_html=True)

exam_col1, exam_col2, exam_col3 = st.columns(3)

with exam_col1:

    st.markdown("""
    <div class="card">

    <div class="card-title">
     School & Scholarship
    </div>

    <div class="card-text">

    • Class 1 to 12  
    • SSC  
    • HSC  
    • Olympiads  
    • NMMS  
    • Scholarship Exams  

    </div>

    </div>
    """, unsafe_allow_html=True)

with exam_col2:

    st.markdown("""
    <div class="card">

    <div class="card-title">
     Competitive Exams
    </div>

    <div class="card-text">

    • NEET  
    • JEE  
    • CET  
    • UPSC  
    • MPSC  
    • NET / SET  

    </div>

    </div>
    """, unsafe_allow_html=True)

with exam_col3:

    st.markdown("""
    <div class="card">

    <div class="card-title">
     Global Education
    </div>

    <div class="card-text">

    • IELTS  
    • TOEFL  
    • SAT  
    • GRE  
    • GMAT  
    • PhD Entrance  

    </div>

    </div>
    """, unsafe_allow_html=True)

# ==============================
# SECURITY FEATURES
# ==============================

st.markdown("""
<div class="section-title">
 Security & Reliability
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text">

 Hidden API Keys  
 File Validation  
 Upload Restrictions  
 Error Handling  
 Session State Protection  
 SQLite Database Security  
 Streamlit Cloud Deployment  
 HTTPS Ready Infrastructure  

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# PRESENTATION READY SECTION
# ==============================

st.markdown("""
<div class="section-title">
 Capstone Highlights
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">

<div class="card-text">

 Real-world Educational Problem Solving  
 AI Powered Student Assistance  
 Rural India Focused Innovation  
 Multi-language Accessibility  
 Centralized Educational Ecosystem  
 Scalable Cloud Deployment  
 IIT-Level Product Design Thinking  

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# FINAL FOOTER
# ==============================

st.markdown("""
<div style='text-align:center; padding:30px; color:white;'>
<h2>Dnyaneshwar Gawalikar</h2>
<p>Capstone Project - IIT Patna</p>
</div>
""", unsafe_allow_html=True)
.footer-box {
    margin-top:70px;
    padding:30px;
    border-radius:24px;

    background: linear-gradient(135deg,
        rgba(255,193,7,0.08),
        rgba(255,255,255,0.03));

    border:1px solid rgba(255,255,255,0.08);

    text-align:center;
}
}
  
 
    border:1px solid rgba(255,255,255,0.08);

    text-align:center;
}




background: linear-gradient(145deg, rgba(255,193,7,0.08), rgba(255,255,255,0.03));
border:1px solist.markdown("""
<div style='text-align:center; padding:30px; color:white;'>
<h2>Dnyaneshwar Gawalikar</h2>
<p>Capstone Project - IIT Patna</p>
</div>
""", unsafe_allow_html=True)d rgba(255,255,255,0.08);


<h1 style="color:#FFD54F; font-size:42px;">
“शिका, स्पर्धा करा, यशस्वी व्हा — हेच आमचं ध्येय!”
</h1>

<h2 style="color:white; margin-top:20px;">
Dnyaneshwar Gawalikar
</h2>

<p style="color:#cccccc; font-size:18px;">
Capstone Project — IIT Patna
</p>

<p style="color:#aaaaaa;">
AI Powered Indian Education Platform
</p>

</div>
""", unsafe_allow_html=True)

<br>

AI Powered Indian Education Platform

</p>

</div>
""", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="card">
      <div class="card-title">
<div class="card-title">
E-Books & Syllabus
</div>

        <div class="card-text">
        Direct links to books,
        syllabus and study material.
        </div>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
         Practice Tests
        </div>

        <div class="card-text">
        MCQ quizzes for NEET,
        JEE, UPSC and MPSC.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="card">
        <div class="card-title">
         Video Lessons
        </div>

        <div class="card-text">
        AI powered educational
        videos and lectures.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# SECOND ROW
# ==============================

g1, g2, g3 = st.columns(3)

with g1:
    st.markdown("""
    <div class="card">
        <div class="card-title">
         Defence & Police
        </div>

        <div class="card-text">
        NDA, CDS, Agniveer
        and Police Bharti guidance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
         Research Hub
        </div>

        <div class="card-text">
        PhD research support,
        journals and innovation tools.
        </div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    st.markdown("""
    <div class="card">
        <div class="card-title">
         Global Education
        </div>

        <div class="card-text">
        IELTS, TOEFL, SAT,
        GRE and abroad scholarships.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# TECH STACK
# ==============================

st.markdown(
    '<div class="section-title"> Technology Stack</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<div class="card-text">

Frontend - Streamlit
Backend - Python
AI - Google Gemini API
Database - SQLite
Charts - Plotly
Deployment - Streamlit Cloud  

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# FUTURE SCOPE
# ==============================

st.markdown(
    '<div class="section-title"> Future Scope</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<div class="card-text">

 AI Voice Mentor  
 Offline Rural Learning Mode  
 Android Application  
 AI Mock Interviews  
 National Scholarship Engine  
 Smart Career Recommendation System  
 Village Learning Hub Integration  

</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# IMPACT
# ==============================

st.markdown(
    '<div class="section-title"> Impact</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<div class="card-text">

 Designed for Rural India  
 Multi-language Education Access  
 Free Government Resources  
 Competitive Exam Support  
 AI Powered Learning Assistance  
 Centralized Education Ecosystem  

</div>

</div>"Shika, Spardha Kara, Yashasvi Vha - Hech Aamcha Dhyey!"
""", unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================

st.markdown("""
<div class="footer-box">

<div class="footer-text">
"शिका, स्पर्धा करा, यशस्वी व्हा - हेच आमचं ध्येय!"
</div>

<br>

<div style="font-size:18px; color:rgba(255,255,255,0.7);">

Built By Dnyaneshwar Gawalikar
<br><br>

<br>
AI Powered Indian Education Platform

</div>

</div>
""", unsafe_allow_html=True)
# ==============================
# MODERN GLOBAL UI DESIGN
# ABHYAS KRANTI NEW
# Paste this BELOW st.set_page_config()
# ==============================

st.markdown("""
<style>

/* ------------------------------
MAIN APP
------------------------------ */

.stApp {
    background: linear-gradient(
     
        #050816 0%,
        #0b1023 40%,
        #111827 100%
    );
    color: white;
    font-family: 'Inter', sans-serif;
}

/* ------------------------------
SIDEBAR
------------------------------ */

section[data-testid="stSidebar"] {
    background: rgba(5, 10, 25, 0.95);st.markdown("""
<style>

.footer-box {
    margin-top: 50px;
    background: linear-gradient(135deg, rgba(255,193,7,0.08), rgba(255,255,255,0.03));
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.footer-text {
    font-size: 22px;
    color: #ffd54f;
    font-weight: bold;
}

st.markdown("""
<div style='text-align:center; padding:30px; color:white;'>
<h2>Dnyaneshwar Gawalikar</h2>
<p>Capstone Project - IIT Patna</p>
</div>
""", unsafe_allow_html=True)

/* ------------------------------

/* ------------------------------
SEARCH BOX
------------------------------ */

.stTextInput input {
    background: rgba(255,255,255,0.06) !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    border-radius: 16px !important;

    color: white !important;

    height: 55px !important;

    font-size: 16px !important;
}

/* ------------------------------
STAT CARDS
------------------------------ */

.stat-card {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.04),
            rgba(255,255,255,0.02)
        );

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 35px;

    text-align: center;

    transition: 0.3s ease;

    backdrop-filter: blur(12px);

    box-shadow:
        0 6px 20px rgba(0,0,0,0.35);
}

.stat-card:hover {
    transform: translateY(-6px);
    border-color: rgba(255,193,7,0.4);
}

.stat-number {
    font-size: 52px;
    font-weight: 900;
    color: white;
}

.stat-label {
    font-size: 18px;
    color: rgba(255,255,255,0.7);
}

/* ------------------------------
FEATURE CARDS
------------------------------ */

.feature-card {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.04),
            rgba(255,255,255,0.02)
        );

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 28px;

    transition: 0.3s ease;

    height: 100%;
}

.feature-card:hover {
    transform: translateY(-5px);

    border-color: rgba(255,193,7,0.35);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.35);
}

.feature-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 10px;
}

.feature-description {
    color: rgba(255,255,255,0.72);
    line-height: 1.7;
    font-size: 16px;
}

/* ------------------------------
SECTION TITLE
------------------------------ */

.section-title {
    font-size: 42px;
    font-weight: 900;
    margin-top: 40px;
    margin-bottom: 30px;
}

/* ------------------------------
FOOTER
------------------------------ */
.footer-box {
    margin-top:70px;
    padding:30px;
    border-radius:24px;

    background: linear-gradient(135deg,
        rgba(255,193,7,0.08),
        rgba(255,255,255,0.03));

    border:1px solid rgba(255,255,255,0.08);

    text-align:center;
}


.footer-text {
    font-size: 22px;
    color: #ffd54f;
    font-weight: 700;
}

/* ------------------------------
HIDE STREAMLIT
------------------------------ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================

st.markdown("""
<div class="hero-container">

<div class="hero-badge">
 A SOCIAL INITIATIVE BY DR. DNYANESHWAR GAWALIKAR
</div>

<div class="hero-title">
Empowering Students from
<br>
<span class="hero-highlight">
Class 1 to Global Careers
</span>
</div>

<div class="hero-subtitle">
क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची!
</div>

<div class="hero-description">
Free resources, AI mentorship, scholarship guidance,
competitive exam support and global education access
for every student across India.
</div>

</div>
""", unsafe_allow_html=True)

# ==============================
# SEARCH BAR
# ==============================

search = st.text_input(
    "",
    placeholder=" Search exams, scholarships, books, careers..."
)

# ==============================
# ACTION BUTTONS
# ==============================

col1, col2, col3 = st.columns(3)

with col1:
    st.button(" Explore Sections")

with col2:
    st.button(" Take Free Quiz")

with col3:
    st.button(" Watch Video Lessons")

# ==============================
# STATISTICS CARDS
# ==============================

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">10,000+</div>
        <div class="stat-label">Students</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">50+</div>
        <div class="stat-label">Exams</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">500+</div>
        <div class="stat-label">Scholarships</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Free Access</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# FOOTER
# ==============================

st.markdown("""
<div class="footer-box">

<div class="footer-text">
“शिका, स्पर्धा करा, यशस्वी व्हा — हेच आमचं ध्येय!”
</div>

<br>

<div style="color: rgba(255,255,255,0.7); font-size:18px;">
— Dr. Dnyaneshwar Gawalikar
</div>

</div>
""", unsafe_allow_html=True)
# ---------------- GEMINI SETUP ----------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-flash")
# ---------------- DATABASE ----------------

conn = sqlite3.connect("abhyas_kranti.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    exam TEXT,
    study_hours INTEGER,
    score INTEGER
)
""")

conn.commit()

# ---------------- SIDEBAR ----------------

st.sidebar.title(" Abhyas Kranti NEW")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "AI Mentor",
        "Study Planner",
        "Exams",
        "Scholarships",
        "Notes",
        "Progress Dashboard"
    ]
)

# ---------------- HOME ----------------

if menu == "Home":

    st.title(" Abhyas Kranti NEW")

    st.subheader("AI Powered Indian Education Platform")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Students", "10,000+")

    with col2:
        st.metric("Exams", "50+")

    with col3:
        st.metric("Scholarships", "500+")

    st.markdown("---")

    st.write("""
    ### Features
    - AI Mentor
    - Study Planner
    - Scholarship Guidance
    - Competitive Exam Support
    - Rural Student Support
    - Notes Upload
    - Progress Tracking
    """)

# ---------------- AI MENTOR ----------------

elif menu == "AI Mentor":

    st.title(" AI Mentor")

    user_input = st.text_input("Ask your question")

    if st.button("Get Answer"):

        if user_input.strip() == "":
            st.warning("Please enter a question.")

        else:

            try:

                response = model.generate_content(user_input)

                st.success("Answer")

                st.write(response.text)

            except Exception as e:

                st.error(f"Error: {e}")

# ---------------- STUDY PLANNER ----------------

elif menu == "Study Planner":

    st.title(" Study Planner")

    exam = st.selectbox(
        "Select Exam",
        ["NEET", "JEE", "UPSC", "MPSC", "NDA"]
    )

    weak_subject = st.text_input("Weak Subject")

    hours = st.slider("Study Hours", 1, 12, 6)

    target = st.number_input("Target Marks", 0, 720, 500)

    if st.button("Generate Plan"):

        st.success("Study Plan Generated")

        st.write(f"""
        ### Smart Study Plan

        - Exam: {exam}
        - Weak Subject: {weak_subject}
        - Daily Hours: {hours}
        - Target Score: {target}

        ### Recommended Schedule

        Morning:
        - Revision

        Afternoon:
        - Practice Questions

        Evening:
        - Mock Tests

        Night:
        - NCERT Reading
        """)

# ---------------- EXAMS ----------------

elif menu == "Exams":

    st.title(" Exams")

    exams = [
        "SSC",
        "HSC",
        "CET",
        "NEET",
        "JEE",
        "NDA",
        "CDS",
        "SSB",
        "UPSC",
        "MPSC",
        "NET",
        "SET",
        "Police Bharti",
        "Agniveer",
        "CUET",
        "GRE",
        "GMAT",
        "IELTS",
        "TOEFL",
        "SAT",
        "PhD Entrance"
    ]

    for exam in exams:
        st.info(exam)

# ---------------- SCHOLARSHIPS ----------------

elif menu == "Scholarships":

    st.title(" Scholarships")

    scholarships = [
        "Class 1-12 Scholarships",
        "State Scholarships",
        "Central Government Scholarships",
        "Minority Scholarships",
        "PhD Fellowships",
        "International Scholarships",
        "Study Abroad Scholarships"
    ]

    for item in scholarships:
        st.success(item)

# ---------------- NOTES ----------------

elif menu == "Notes":

    st.title(" Notes")

    Path("notes").mkdir(exist_ok=True)

    
# ---------------- NOTES ----------------

elif menu == "Notes":

    st.title(" Notes")

    Path("notes").mkdir(exist_ok=True)

    MAX_FILE_SIZE = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = ["pdf"]

    uploaded_file = st.file_uploader(
        "Upload PDF Notes",
        type=["pdf"]
    )

    if uploaded_file is not None:

        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension not in ALLOWED_EXTENSIONS:

            st.error("Only PDF files are allowed.")

        elif uploaded_file.size > MAX_FILE_SIZE:

            st.error("File size exceeds 5 MB.")

        else:

            save_path = Path("notes") / uploaded_file.name

            with open(save_path, "wb") as f:

                f.write(uploaded_file.read())

            st.success("File Uploaded Successfully")

    st.subheader("Available Notes")

    notes = list(Path("notes").glob("*.pdf"))

    for note in notes:

        with open(note, "rb") as f:

            st.download_button(
                label=f"Download {note.name}",
                data=f,
                file_name=note.name,
                mime="application/pdf"
            )
  
    for note in notes:

        with open(note, "rb") as f:

            st.download_button(
                label=f"Download {note.name}",
                data=f,
                file_name=note.name,
                mime="application/pdf"
            )

# ---------------- PROGRESS DASHBOARD ----------------

elif menu == "Progress Dashboard":

    st.title(" Progress Dashboard")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        exam = st.text_input("Exam")

        study_hours = st.slider("Study Hours", 1, 12, 5)

        score = st.slider("Mock Test Score", 0, 720, 300)

        submit = st.form_submit_button("Save")

    if submit:

        cursor.execute("""
        INSERT INTO students (
            name,
            exam,
            study_hours,
            score
        )
        VALUES (?, ?, ?, ?)
        """, (
            name,
            exam,
            study_hours,
            score
        ))

        conn.commit()

        st.success("Data Saved")

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if not df.empty:

        st.dataframe(df)

        fig = px.bar(
            df,
            x="name",
            y="score",
            color="exam",
            title="Student Performance"
        )

        st.plotly_chart(fig, use_container_width=True)# ---------------- MODERN UI ----------------


MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = ["pdf"]

uploaded_file = st.file_uploader(
    "Upload PDF Notes",
    type=["pdf"]
)

if uploaded_file is not None:

    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:

        st.error("Only PDF files are allowed.")

    elif uploaded_file.size > MAX_FILE_SIZE:

        st.error("File size exceeds 5 MB.")

    else:

        save_path = Path("notes") / uploaded_file.name

        with open(save_path, "wb") as f:

            f.write(uploaded_file.read())

        st.success("File Uploaded Successfully")
if len(user_input) > 1000:
    st.warning("Question too long.")

APP_PASSWORD = "abhyas123"

password = st.sidebar.text_input(
    "Admin Password",
    type="password"
)

if password != APP_PASSWORD:
    st.warning("Enter password")
    st.stop()
  

    # FULL APP CODE

try:

    response = model.generate_content(user_input)

    st.success("Answer")

    st.write(response.text)

except Exception as e:

    st.error(f"Error: {e}")
if "last_request" not in st.session_state:
    st.session_state.last_request = datetime.now()
    Path("notes").mkdir(
    exist_ok=True
)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
