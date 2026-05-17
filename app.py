import streamlit as st

st.set_page_config(
    page_title="Abhyas Kranti NEW",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Abhyas Kranti NEW")

st.write("AI Powered Educational Platform for Rural India")

st.header("🎯 Objectives")

st.write("""
- Centralized education ecosystem
- AI-powered student guidance
- Scholarship awareness
- Competitive exam support
- Rural India accessibility
- Multi-language learning support
""")

st.header("⚠️ Problem Statement")

st.write("""
- Lack of centralized educational resources
- Expensive coaching ecosystem
- Scholarship awareness issues
- Career guidance gap
- Language barriers
""")

st.header("💡 Our Solution")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🤖 AI Mentor")

with col2:
    st.info("📅 Smart Planner")

with col3:
    st.info("🎓 Scholarship Engine")

st.header("🛠 Technology Stack")

st.write("""
- Frontend → Streamlit
- Backend → Python
- AI → Gemini API
- Database → SQLite
- Deployment → Streamlit Cloud
""")

st.header("🌍 Impact")

st.write("""
- Designed for Rural India
- Multi-language Education Access
- Competitive Exam Support
- AI Powered Learning Assistance
""")

st.success("शिका, स्पर्धा करा, यशस्वी व्हा – हेच आमचं ध्येय!")
