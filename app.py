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

    uploaded_file = st.file_uploader(
        "Upload PDF Notes",
        type=["pdf"]
    )

    if uploaded_file is not None:

        save_path = Path("notes") / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("File Uploaded")

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

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
}

h1, h2, h3, h4, h5 {
    color: white !important;
    font-weight: 700;
}

p, label, div {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 3rem;
    border: none;
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    font-size: 16px;
    font-weight: 600;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    background-color: rgba(255,255,255,0.08);
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
}

.stSelectbox > div > div {
    border-radius: 12px;
}

.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.hero-box {
    background: linear-gradient(
        135deg,
        rgba(37,99,235,0.25),
        rgba(124,58,237,0.25)
    );
    padding: 40px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 30px;
}

.feature-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = ["pdf"]
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
