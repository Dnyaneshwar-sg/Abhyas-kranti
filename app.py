from pathlib import Path

code = r'''import streamlit as st

st.set_page_config(
    page_title="Abhyas Kranti NEW",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background: linear-gradient(to bottom, #111827, #1e293b);
    color: white;
}
.big-title {
    font-size: 48px;
    font-weight: bold;
    color: #facc15;
}
.section-title {
    font-size: 32px;
    font-weight: bold;
    margin-top: 30px;
    color: #fde047;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🎓 Abhyas Kranti NEW</p>', unsafe_allow_html=True)

st.write("AI Powered Educational Platform for Rural India")

st.markdown('<p class="section-title">🎯 Objectives</p>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
✅ Centralized education ecosystem<br>
✅ AI-powered student guidance<br>
✅ Scholarship awareness<br>
✅ Competitive exam support<br>
✅ Rural India accessibility<br>
✅ Multi-language learning support
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">⚠️ Problem Statement</p>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
• Lack of centralized educational resources<br>
• Expensive coaching ecosystem<br>
• Scholarship awareness issues<br>
• Career guidance gap<br>
• Language barriers
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">💡 Our Solution</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🤖 AI Mentor</h3>
    AI powered educational guidance and support.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>📅 Smart Planner</h3>
    Personalized study planning for students.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>🎓 Scholarship Engine</h3>
    Scholarship discovery and guidance.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="section-title">🛠 Technology Stack</p>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
✅ Frontend → Streamlit<br>
✅ Backend → Python<br>
✅ AI → Gemini API<br>
✅ Database → SQLite<br>
✅ Deployment → Streamlit Cloud
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">🌍 Impact</p>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
✅ Designed for Rural India<br>
✅ Multi-language Education Access<br>
✅ Competitive Exam Support<br>
✅ AI Powered Learning Assistance
</div>
""", unsafe_allow_html=True)

st.markdown("""
<hr>
<center>
<h2>“शिका, स्पर्धा करा, यशस्वी व्हा – हेच आमचं ध्येय!”</h2>
<h3>Dnyaneshwar Gawalikar</h3>
<p>Capstone Project – IIT Patna</p>
</center>
""", unsafe_allow_html=True)
'''

path = Path("/mnt/data/app.py")
path.write_text(code, encoding="utf-8")

print(f"Saved clean Streamlit app to {path}")
