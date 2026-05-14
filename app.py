
import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.express as px
from pathlib import Path
import google.generativeai as genai
st.set_page_config(
    page_title="अभ्यास क्रांती"
    ,
    page_icon="📚",
    layout="wide"
)
st.title("🚀 Abhyas Kranti NEW")

# -----------------------------
# Folders
# -----------------------------
Path("notes").mkdir(exist_ok=True)
Path("downloads").mkdir(exist_ok=True)

# -----------------------------
# Database Setup
# -----------------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    exam TEXT,
    study_hours INTEGER,
    completed_chapters INTEGER,
    mock_score INTEGER
)
""")
conn.commit()

# -----------------------------
# Language Support
# -----------------------------
languages = {
    "English": {
        "title": "Abhyas Kranti",
        "welcome": "Free Education Platform for Rural Students",
        "chat_placeholder": "Ask your question..."
    },
    "मराठी": {
        "title": "अभ्यास क्रांती",
        "welcome": "ग्रामीण विद्यार्थ्यांसाठी मोफत शिक्षण प्लॅटफॉर्म",
        "chat_placeholder": "तुमचा प्रश्न विचारा..."
    },
    "हिन्दी": {
        "title": "अभ्यास क्रांति",
        "welcome": "ग्रामीण छात्रों के लिए मुफ्त शिक्षा मंच",
        "chat_placeholder": "अपना प्रश्न पूछें..."
    }
}

selected_lang = st.sidebar.selectbox(
    "🌐 Language",
    list(languages.keys())
)

lang = languages[selected_lang]

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="📚 Abhyas Kranti",
        options=[
            "Home",
            "Exams",
            "Notes",
            "AI Mentor",
            "Study Planner",
            "Progress Dashboard"
        ],
        icons=[
            "house",
            "book",
            "file-earmark",
            "robot",
            "calendar",
            "bar-chart"
        ],
        default_index=0
    )

# -----------------------------
# HOME
# -----------------------------
if selected == "Home":

    st.title(f"🚀 {lang['title']}")
    st.subheader(lang["welcome"])

    st.info("Empowering Maharashtra rural students through free education and AI learning.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Students Supported", "10,000+")

    with col2:
        st.metric("Free Notes", "500+")

    with col3:
        st.metric("AI Support", "24/7")

    st.markdown("---")

    st.header("🎯 Features")

    st.write("""
    - 📚 Competitive Exam Preparation
    - 🤖 AI Mentor
    - 📥 Offline Notes
    - 📅 Study Planner
    - 📊 Progress Tracking
    - 🌐 Multi-language Support
    """)

    st.success("“Education is the most powerful weapon to change the world.”")

# -----------------------------
# EXAMS
# -----------------------------
with st.chat_message("assistant"):
    if "reply" in locals():
        st.write(reply)

# -------------------------
# STUDY PLANNER
# -------------------------

if selected == "Study Planner":
    exam_tabs = st.tabs([
        "School",
        "Higher Education",
        "Competitive Exams"
    ])

    with exam_tabs[0]:
        st.subheader("🏫 School Education")
        st.write("""
        - Class 1 to 12
        - SSC
        - HSC
        - Scholarship Exams
        """)

    with exam_tabs[1]:
        st.subheader("🎓 Higher Education")
        st.write("""
        - CET
        - NEET
        - JEE
        - NDA
        - CUET
        - NET
        - SET
        """)

    with exam_tabs[2]:
        st.subheader("🏆 Competitive Exams")
        st.write("""
        - UPSC
        - MPSC
        - Army
        - Navy
        - Air Force
        - CDS
        """)

# -----------------------------
# NOTES
# -----------------------------
elif selected == "Notes":

    st.title("📝 Notes & Study Material")

    uploaded_file = st.file_uploader(
        "Upload PDF Notes",
        type=["pdf"]
    )

    if uploaded_file is not None:
        save_path = Path("notes") / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"{uploaded_file.name} uploaded successfully!")

    st.subheader("📂 Available Notes")

    notes_files = list(Path("notes").glob("*.pdf"))

    if notes_files:
        for file in notes_files:
            with open(file, "rb") as f:
                st.download_button(
                    label=f"📥 Download {file.name}",
                    data=f,
                    file_name=file.name,
                    mime="application/pdf"
                )
    else:
        st.info("No notes uploaded yet.")

# -----------------------------
# AI MENTOR
# -----------------------------
elif selected == "AI Mentor":

    st.title("🤖 AI Mentor")

    user_input = st.text_input("Ask your question")
    send = st.button("Send")

    if send and user_input.strip():

        with st.chat_message("user"):
            st.write(user_input)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash-latest")

response = model.generate_content(user_input)
reply = response.text

response = model.generate_content(user_input)
reply = response.text

st.write(reply)
response = model.generate_content(user_input)
reply = response.text

with st.chat_message("assistant"):
    st.write(reply)  

if selected == "Study Planner":
        
    st.title("📅 Smart Study Planner")

    exam = st.text_input("Exam Name")
    weak_subject = st.text_input("Weak Subject")
    hours = st.slider("Daily Study Hours", 1, 12, 4)
    target = st.number_input("Target Marks", 0, 720, 500)

    if st.button("Generate Study Plan"):

        st.success("Study Plan Generated!")

        st.write(f"""
        ## 📌 Daily Plan

        - Morning: Revision
        - Afternoon: Practice Questions
        - Evening: Mock Tests
        - Night: NCERT Reading

        ## 🎯 Target
        - Exam: {exam}
        - Weak Subject: {weak_subject}
        - Daily Hours: {hours}
        - Target Score: {target}
        """)

# -----------------------------
# PROGRESS DASHBOARD
# -----------------------------
elif selected == "Progress Dashboard":

    st.title("📊 Student Progress Dashboard")

    with st.form("student_form"):

        name = st.text_input("Student Name")
        exam = st.text_input("Exam")
        study_hours = st.slider("Study Hours", 1, 12, 5)
        chapters = st.slider("Completed Chapters", 0, 100, 10)
        mock_score = st.slider("Mock Test Score", 0, 720, 300)

        submit = st.form_submit_button("Save Progress")

    if submit:

        cursor.execute("""
        INSERT INTO students (
            name,
            exam,
            study_hours,
            completed_chapters,
            mock_score
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            exam,
            study_hours,
            chapters,
            mock_score
        ))

        conn.commit()

        st.success("Progress Saved Successfully!")

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if not df.empty:

        st.subheader("📋 Student Records")
        st.dataframe(df)

        fig = px.bar(
            df,
            x="name",
            y="mock_score",
            title="Mock Test Scores"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No student data available.")
