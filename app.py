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
    page_icon="📘",
    layout="wide"
)
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
        135deg,
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
    background: rgba(5, 10, 25, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

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
    margin-top: 50px;

    background:
        linear-gradient(
            135deg,
            rgba(255,193,7,0.08),
            rgba(255,255,255,0.03)
        );

    border-radius: 24px;

    padding: 30px;

    border: 1px solid rgba(255,255,255,0.08);

    text-align: center;
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
🚀 A SOCIAL INITIATIVE BY DR. DNYANESHWAR GAWALIKAR
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
    placeholder="🔍 Search exams, scholarships, books, careers..."
)

# ==============================
# ACTION BUTTONS
# ==============================

col1, col2, col3 = st.columns(3)

with col1:
    st.button("📚 Explore Sections")

with col2:
    st.button("🧠 Take Free Quiz")

with col3:
    st.button("🎥 Watch Video Lessons")

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
# FEATURES
# ==============================

st.markdown(
    '<div class="section-title">⚡ Quick Access</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        📘 E-Books & Syllabus
        </div>

        <div class="feature-description">
        Direct links to books, syllabus,
        notes and study materials.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        🧠 Practice Tests
        </div>

        <div class="feature-description">
        MCQ quizzes for NEET, JEE,
        UPSC, MPSC and more.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        🎥 Video Lessons
        </div>

        <div class="feature-description">
        Free educational videos,
        lectures and AI explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# SECOND ROW
# ==============================

f4, f5, f6 = st.columns(3)

with f4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        🛡 Defence & Police
        </div>

        <div class="feature-description">
        NDA, CDS, Agniveer,
        Police Bharti preparation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        🔬 Research Hub
        </div>

        <div class="feature-description">
        PhD guidance, research tools,
        journals and innovation support.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
        🌍 Global Education
        </div>

        <div class="feature-description">
        IELTS, TOEFL, SAT, GRE,
        GMAT and abroad scholarships.
        </div>
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

st.sidebar.title("📘 Abhyas Kranti NEW")

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

    st.title("🚀 Abhyas Kranti NEW")

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

    st.title("🤖 AI Mentor")

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

    st.title("📅 Study Planner")

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

    st.title("📝 Exams")

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

    st.title("🎓 Scholarships")

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

    st.title("📚 Notes")

    Path("notes").mkdir(exist_ok=True)

    
# ---------------- NOTES ----------------

elif menu == "Notes":

    st.title("📚 Notes")

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

    st.title("📊 Progress Dashboard")

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
