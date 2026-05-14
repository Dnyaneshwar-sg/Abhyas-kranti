import streamlit as st
import google.generativeai as genai
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Abhyas Kranti NEW",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# GEMINI API
# -----------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📚 Abhyas Kranti")

selected = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "AI Mentor",
        "Study Planner",
        "Progress Dashboard"
    ]
)

# -----------------------------
# HOME
# -----------------------------
if selected == "Home":

    st.title("🚀 Abhyas Kranti NEW")

    st.subheader("Free Education Platform")

    st.write("""
    Welcome to Abhyas Kranti.

    Features:
    - AI Mentor
    - Study Planner
    - Progress Dashboard
    """)

# -----------------------------
# AI MENTOR
# -----------------------------
elif selected == "AI Mentor":

    st.title("🤖 AI Mentor")

    user_input = st.text_input("Ask your question")

    if st.button("Send"):

        if user_input.strip() == "":
            st.warning("Please enter a question")

        else:

          model = genai.GenerativeModel("models/gemini-1.5-flash")

response = model.generate_content(user_input)
            reply = response.text

            st.success("Answer")

            st.write(reply)

# -----------------------------
# STUDY PLANNER
# -----------------------------
elif selected == "Study Planner":

    st.title("📝 Study Planner")

    exam = st.text_input("Exam Name")

    weak_subject = st.text_input("Weak Subject")

    hours = st.slider(
        "Daily Study Hours",
        1,
        12,
        4
    )

    target = st.number_input(
        "Target Marks",
        0,
        720,
        500
    )

    if st.button("Generate Plan"):

        st.success("Study Plan Generated")

        st.write(f"""
### 📅 Daily Plan

- Morning : Revision
- Afternoon : Practice Questions
- Evening : Mock Test
- Night : NCERT Reading

### 🎯 Target

- Exam : {exam}
- Weak Subject : {weak_subject}
- Study Hours : {hours}
- Target Score : {target}
""")

# -----------------------------
# PROGRESS DASHBOARD
# -----------------------------
elif selected == "Progress Dashboard":

    st.title("📊 Progress Dashboard")

    name = st.text_input("Student Name")

    physics = st.slider("Physics", 0, 180, 90)

    chemistry = st.slider("Chemistry", 0, 180, 90)

    biology = st.slider("Biology", 0, 360, 180)

    total = physics + chemistry + biology

    st.subheader("Total Score")

    st.write(total)

    data = {
        "Subject": ["Physics", "Chemistry", "Biology"],
        "Marks": [physics, chemistry, biology]
    }

    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Subject"))
