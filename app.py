import streamlit as st
import sqlite3
import pandas as pd

# १. डेटाबेस सेटअप (विद्यार्थ्यांचे निकाल साठवण्यासाठी)
def init_db():
    conn = sqlite3.connect('abhyas_kranti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (name TEXT, score INTEGER, total INTEGER)''')
    conn.commit()
    conn.close()

def main():
    # २. ॲपचे नाव आणि डिझाइन
    st.set_page_config(page_title="अभ्यास क्रांती", page_icon="📚")
    st.title("📚 अभ्यास क्रांती")
    st.subheader("स्पर्धा परीक्षा तयारी केंद्र")

    # ३. साइडबार मेनू
    menu = ["होम", "सराव परीक्षा", "निकाल", "माहिती","AI मार्गदर्शक"]
    choice = st.sidebar.selectbox("निवडा", menu)

    init_db()

    # ४. होम विभाग
    if choice == "होम":
        st.write("### स्वागत आहे!")
        st.info("तुमच्या स्पर्धा परीक्षेच्या तयारीसाठी हे एक उत्तम व्यासपीठ आहे.")
        st.write("येथे तुम्ही विविध विषयांचा सराव करू शकता आणि तुमचा निकाल पाहू शकता.")
        
    # ५. सराव परीक्षा विभाग
    elif choice == "sराव परीक्षा":
        st.write("### सामान्य ज्ञान सराव")
        with st.form(key='quiz_form'):
            q1 = st.radio("१. महाराष्ट्राची राजधानी कोणती?", ("पुणे", "मुंबई", "नागपूर", "छत्रपती संभाजीनगर"))
            submit_button = st.form_submit_button(label='निकाल पहा')
            
            if submit_button:
                score = 1 if q1 == "मुंबई" else 0
                st.success(f"तुमचा स्कोर: {score}/1")
                
                # निकाल डेटाबेसमध्ये जतन करणे
                conn = sqlite3.connect('abhyas_kranti.db')
                c = conn.cursor()
                c.execute("INSERT INTO results (name, score, total) VALUES (?, ?, ?)", ("विद्यार्थी", score, 1))
                conn.commit()
                conn.close()

    # ६. निकाल विभाग
    elif choice == "निकाल":
        st.write("### मागील निकाल")
        conn = sqlite3.connect('abhyas_kranti.db')
        try:
            df = pd.read_sql_query("SELECT * FROM results", conn)
            st.dataframe(df)
        except:
            st.warning("अद्याप कोणतेही निकाल उपलब्ध नाहीत.")
        finally:
            conn.close()

    # ७. फुटर माहिती (IIT Patna Capstone Project)
    st.sidebar.markdown("---")
    st.sidebar.write("© 2026 Abhyas Kranti | IIT Patna")
    st.sidebar.write("Capstone Project | Dr. Dnyaneshwar Gawalikar")

if __name__ == '__main__':
    main()
import streamlit as st
import pandas as pd

# Page Configuration (जागतिक दर्जाचे सेटिंग)
st.set_page_config(
    page_title="अभ्यास क्रांती | Abhyas Kranti",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #fbbf24;
        color: black;
        font-weight: bold;
    }
    .title-text {
        text-align: center;
        color: #fbbf24;
    }
    </style>
    """, unsafe_allow_headers=True)

# Header Section
st.markdown("<h1 class='title-text'>अभ्यास क्रांती (Abhyas Kranti)</h1>", unsafe_allow_headers=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची! | By Dr. Dnyaneshwar Gawalikar</p>", unsafe_allow_headers=True)

# Sidebar for Navigation
st.sidebar.title("Main Menu")
selection = st.sidebar.radio("विभाग निवडा:", ["Home", "E-Books", "Practice Tests", "AI Study Planner", "UPSC/MPSC Guidance"])

if selection == "Home":
    st.subheader("स्वागत आहे!")
    st.write("हे पोर्टल ग्रामीण भागातील विद्यार्थ्यांना १ ली ते UPSC पर्यंतच्या सर्व शैक्षणिक गरजांसाठी मोफत मार्गदर्शन पुरवते.")
    import streamlit as st
import random # For fallback quiz generation

# १. जागतिक दर्जाची पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="Abhyas Kranti | ग्लोबल एड्युकेशन प्लॅटफॉर्म",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# २. प्रीमियम डिझाइनसाठी Custom CSS (Global Look)
st.markdown("""
<style>
    /* मुख्य बॅकग्राउंड आणि फॉन्ट */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Poppins', sans-serif;
    }
    
    /* युनिक हेडर डिझाइन */
    .header-style {
        text-align: center;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-bottom: 3px solid #fbbf24;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* बटनांचे जागतिक डिझाइन */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background-color: #fbbf24;
        color: black !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 10px rgba(251,191,36,0.3);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(251,191,36,0.6);
    }
    
    /* इन्फो बॉक्स स्टाइल */
    div.stAlert {
        border-radius: 15px;
        background-color: #1f2937;
        color: #fbbf24;
        border: 1px solid #fbbf24;
    }
    
    /* फुटर */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111827;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        z-index: 99;
    }
</style>
""", unsafe_allow_headers=True)

# ३. बहुभाषिक एआय प्रॉम्पट (Core Logic)
def get_ai_multilingual_prompt(language, topic):
    """import requests

def get_ai_response(user_message, session_id):
    url = "तुमची_N8N_WEBHOOK_URL_येथे_टाका"
    payload = {
        "message": user_message,
        "sessionId": session_id
    }
    response = requests.post(url, json=payload)
    return response.json()['output']
    विद्यार्थ्यांच्या शंकांचे निरसन करण्यासाठी बहुभाषिक प्रॉम्पट.
    इथे 'topic' हे विद्यार्थ्यांच्या प्रश्नाचे नाव आहे.
    """
    prompts = {
        'मराठी': f"""तुम्ही एक जागतिक दर्जाचे एआय शैक्षणिक मार्गदर्शक आहात. मला '{topic}' या विषयावर एका १० वर्षांच्या मुलाला समजेल इतक्या सोप्या भाषेत पण सविस्तर माहिती मराठीत द्या. माहिती देताना उदाहरणे आणि महत्त्वाचे मुद्दे वापरा.""",
        'हिंदी': f"""आप एक ग्लोबल एआई एजुकेशनल गाइड हैं। मुझे '{topic}' इस विषय पर 10 साल के बच्चे को समझ आए इतनी सरल भाषा में लेकिन विस्तृत जानकारी हिंदी में दें। जानकारी देते समय उदाहरणों और महत्वपूर्ण बिंदुओं का उपयोग करें।""",
        'English': f"""You are a global AI educational guide. Provide me with detailed information on the topic '{topic}' in simple language that a 10-year-old child would understand, but in detail, in English. Use examples and key points while providing information."""
    }
    # जर तुमच्याकडे Supabase/OpenAI API असेल तर इथे कनेक्ट करा,
    # नाहीतर आपण एक 'फलक' (Placeholder) मजकूर वापरू.
    return prompts.get(language, prompts['English'])

# ४. मुख्य मजकूर (जागतिक हेडर)
st.markdown("<div class='header-style'>\n"
            "<h1 style='color: #fbbf24; font-size: 2.5rem; margin: 0;'>अभ्यास क्रांती - ग्लोबलाइज्ड एज्युकेशन</h1>\n"
            "<p style='color: #94a3b8; font-size: 1.1rem; margin-top: 10px;'>एक जागतिक दर्जाचे शैक्षणिक व्यासपीठ, जिथे भाषा आता अडथळा नाही.</p>\n"
            "</div>", unsafe_allow_headers=True)

# ५. नेव्हिगेशन आणि विभाग
col1, col2, col3 = st.columns([1.5, 3, 1.5]) # साइडबारऐवजी मुख्य स्क्रीनवर मेनू

with col2:
    selected_language = st.selectbox("तुमची भाषा निवडा / Select your language:", ["मराठी", "हिंदी", "English"])
    
    # विभाग निवड
    section = st.radio("विभाग निवडा / Select Section:", ["📚 मुख्य", "🧠 एआय शंका निरसन", "🖥️ सराव परीक्षा"])
    st.write("---")

    if section == "📚 मुख्य":
        st.subheader("सर्वसमावेशक शिक्षण विभाग")
        st.info("येथे तुम्हाला यूपीएससी/एमपीएससी, नीट, जेई आणि शालेय शिक्षण या सर्व परीक्षांचे जागतिक दर्जाचे साहित्य मोफत मिळेल.")

    elif section == "🧠 एआय शंका निरसन":
        st.subheader("🧠 बहुभाषिक एआय शंका निरसन (Multilingual AI Help)")
        
        # विद्यार्थ्यांचा प्रश्न
        student_question = st.text_input("तुमची शंका किंवा विषय लिहा / Enter your doubt or topic:")
        
        if st.button("शंका निरसन करा (Solve Doubt)"):
            if student_question:
                # प्रॉम्पट तयार करणे
                prompt = get_ai_multilingual_prompt(selected_language, student_question)
                
                with st.spinner("एआय तुमचा अभ्यासक्रम तयार करत आहे..."):
                    # येथे तुमची OpenAI API कॉल कनेक्ट करा
                    # OpenAI_API_KEY = "तुमचा_API_KEY" # सिक्रेट्समध्ये टाका
                    # ... API कॉल ...
                    
                    # तात्पुरता रिस्पॉन्स (Placeholder response)
                    # जर API नसेल तर हे दाखवले जाईल:
                    fallback_response = f"({selected_language}): '{student_question}' या विषयावर अधिक माहिती लवकरच उपलब्ध होईल. कृपया OpenAI API की (OpenAI API Key) तुमच्या 'Secrets' मध्ये टाका."
                    
                    st.markdown(f"<div style='background-color: #1f2937; padding: 20px; border-radius: 10px; border: 1px solid #fbbf24;'>\n"
                                f"<strong>एआय उत्तर / AI Response:</strong><br><br>\n"
                                f"{fallback_response}\n"
                                f"</div>", unsafe_allow_headers=True)
                    
                    # जागतिक लूकसाठी एक 'सेलिब्रेशन' इफेक्ट
                    st.balloons()
            else:
                st.warning("कृपया विषय लिहा / Please enter a topic.")

    elif section == "🖥️ सराव परीक्षा":
        st.subheader("🖥️ सराव परीक्षा केंद्र (Global Practice Tests)")
        st.write("जागतिक दर्जाचे प्रश्नसंच सोडवून तुमची प्रगती तपासा.")

# ६. फुटर
st.markdown("<div class='footer'>\n"
            "© 2026 Abhyas Kranti | Global Education Initiative | Guided by Dr. Dnyaneshwar Gawalikar\n"
            "</div>", unsafe_allow_headers=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **E-Books**\nबालभारती व NCERT पुस्तके")
    with col2:
        st.success("📝 **Practice Tests**\nNEET, JEE, MPSC सराव")
    with col3:
        st.warning("🤖 **AI Planner**\nतुमच्या अभ्यासाचे नियोजन")

elif selection == "AI Study Planner":
    st.subheader("🤖 AI Study Planner (Capstone Project)")
    goal = st.text_input("तुमचे ध्येय काय आहे? (उदा. NEET 2027, MPSC)")
    days = st.slider("किती दिवसांचे नियोजन हवे आहे?", 7, 90, 30)
    
    if st.button("Generate Plan"):
        st.write(f"तुमच्या {goal} साठी {days} दिवसांचा मास्टर प्लॅन तयार होत आहे...")
        # इथे तुमचे Supabase किंवा AI लॉजिक कनेक्ट होईल

elif selection == "Practice Tests":
    st.subheader("📝 सराव परीक्षा विभाग")
    test_type = st.selectbox("परीक्षा निवडा", ["Class 7 Spelling Test", "NEET Mock Test", "MPSC General Studies"])
    st.write(f"{test_type} साठी उपलब्ध साहित्य लवकरच लोड होईल.")

# Footer Section
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em;'>© 2026 Abhyas Kranti | IIT Patna Capstone Project | Managed by Academic Research & Innovation Cell</p>", unsafe_allow_headers=True)
import streamlit as st
import pandas as pd

# १. पेज कॉन्फिगरेशन आणि डिझाइन
st.set_page_config(
    page_title="अभ्यास क्रांती | Abhyas Kranti",
    page_icon="🎓",
    layout="wide"
)

# प्रोफेशनल लूकसाठी डार्क थीम CSS
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stButton>button {
        background-color: #fbbf24;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stSelectbox label, .stTextInput label { color: #fbbf24 !important; }
    .footer { text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 50px; }
    </style>
    """, unsafe_allow_headers=True)

# २. मुख्य शीर्षक (Header)
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🎓 अभ्यास क्रांती (Abhyas Kranti)</h1>", unsafe_allow_headers=True)
st.markdown("<p style='text-align: center;'>क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची!</p>", unsafe_allow_headers=True)
st.write("---")

# ३. नेव्हिगेशन मेनू (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=100)
    st.title("मुख्य विभाग")
    choice = st.radio("निवडा:", ["🏠 होम पेज", "📚 स्पर्धा परीक्षा (MPSC/UPSC)", "🧬 NEET/JEE केंद्र", "📖 शालेय शिक्षण (१ ली ते १० वी)", "🤖 AI करिअर प्लॅनर"])

# ४. विभागानुसार मजकूर
if choice == "🏠 होम पेज":
    st.subheader("स्वागत आहे, डॉ. ज्ञानेश्वर गवालिकर सर!")
    st.info("हे पोर्टल ग्रामीण भागातील विद्यार्थ्यांना मोफत आणि दर्जेदार शिक्षण देण्यासाठी समर्पित आहे.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("✅ मोफत ई-पुस्तके")
        st.write("✅ ऑनलाईन सराव परीक्षा")
    with col2:
        st.write("✅ AI आधारित मार्गदर्शन")
        st.write("✅ तज्ज्ञांचे स्टडी प्लॅन्स")

elif choice == "📚 स्पर्धा परीक्षा (MPSC/UPSC)":
    st.subheader("MPSC/UPSC तयारी केंद्र")
    st.write("येथे तुम्हाला चालू घडामोडी, नोट्स आणि सराव प्रश्नसंच मिळतील.")
    if st.button("सराव प्रश्नसंच उघडा"):
        st.write("प्रश्नसंच लोड होत आहे...")

elif choice == "🧬 NEET/JEE केंद्र":
    st.subheader("NEET 2027 तयारी")
    st.write("श्रुती आणि इतर सर्व विद्यार्थ्यांसाठी खास डिझाइन केलेले मॉड्युल्स.")
    st.progress(70) # अभ्यासाची प्रगती दर्शवण्यासाठी
    st.write("तुमचा स्कोर: ३५०/७२० (मागील टेस्ट)")

elif choice == "🤖 AI करिअर प्लॅनर":
    st.subheader("🤖 AI आधारित करिअर आणि अभ्यास नियोजन")
    goal = st.text_input("तुमचे ध्येय लिहा (उदा. मला अधिकारी व्हायचे आहे)")
    if st.button("प्लॅन तयार करा"):
        st.success(f"तुमच्या '{goal}' या ध्येयासाठी AI प्लॅन तयार करत आहे...")
        st.snow() # सेलिब्रेशन इफेक्ट

# ५. प्रोफेशनल फुटर
st.markdown("---")
st.markdown("""
    <div class='footer'>
        © 2026 Abhyas Kranti | IIT Patna Capstone Project | Managed by Academic Research & Innovation Cell<br>
        Guided by Dr. Dnyaneshwar Gawalikar
    </div>
    """, unsafe_allow_headers=True)
# हा कोड तुमच्या AI लॉजिकमध्ये वापरा
messages = [
    {"role": "system", "content": "You are the Abhyas Kranti Global AI Mentor. Respond in Marathi/Hindi/English as requested. Focus on UPSC, NEET, and School Education."},
    {"role": "user", "content": f"विषय: {student_question}. भाषा: {selected_language}. कृपया जागतिक दर्जाचे मार्गदर्शन द्या."}
]
import streamlit as st
import pandas as pd
import sqlite3

# १. पेज कॉन्फिगरेशन (Global Standard)
st.set_page_config(
    page_title="Abhyas Kranti | Global AI Portal",
    page_icon="🌍",
    layout="wide"
)

# २. प्रीमियम डार्क थीम आणि डिझाइन (Custom CSS)
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header-box {
        text-align: center;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 40px;
        border-radius: 20px;
        border-bottom: 4px solid #fbbf24;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #fbbf24;
        color: black !important;
        font-weight: bold;
        border: none;
        height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); background-color: #f59e0b; }
    .footer { text-align: center; padding: 20px; color: #94a3b8; font-size: 0.9rem; }
</style>
""", unsafe_allow_headers=True)

# ३. डेटाबेस सेटअप (SQLite - स्थानिक साठवणुकीसाठी)
def init_db():
    try:
        conn = sqlite3.connect('abhyas_kranti.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_activity 
                     (id INTEGER PRIMARY KEY, topic TEXT, lang TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Database Error: {e}")

init_db()

# ४. मुख्य हेडर
st.markdown("""
<div class='header-box'>
    <h1 style='color: #fbbf24; font-size: 3rem;'>अभ्यास क्रांती</h1>
    <p style='font-size: 1.2rem; color: #94a3b8;'>क्रांती शिक्षणाची, प्रगती ग्रामीण महाराष्ट्राची! | Global AI Mentor</p>
</div>
""", unsafe_allow_headers=True)

# ५. नेव्हिगेशन (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/education.png", width=100)
    st.title("Settings")
    selected_lang = st.selectbox("भाषा निवडा / Language", ["मराठी", "हिंदी", "English"])
    section = st.radio("विभाग / Section", ["🏠 होम", "🤖 AI शंका निरसन", "📚 अभ्यास साहित्य", "📊 प्रगती"])

# ६. विभागानुसार मजकूर
if section == "🏠 होम":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎯 **UPSC/MPSC**\nप्रशासकीय सेवेसाठी परिपूर्ण मार्गदर्शन.")
    with col2:
        st.success("🧬 **NEET/JEE**\nवैद्यकीय व अभियांत्रिकी प्रवेश पूर्व तयारी.")
    with col3:
        st.warning("🏫 **School Education**\n१ ली ते १० वी पर्यंतचे सर्व विषय.")
    
    st.write("---")
    st.subheader("आमचे ध्येय")
    st.write("ग्रामीण भागातील प्रत्येक विद्यार्थ्याला जागतिक दर्जाचे शिक्षण मोफत उपलब्ध करून देणे हेच आमचे उद्दिष्ट आहे.")

elif section == "🤖 AI शंका निरसन":
    st.subheader(f"🧠 AI Doubt Solver ({selected_lang})")
    user_input = st.text_input("तुमची शंका किंवा विषय येथे लिहा...")
    
    if st.button("उत्तर मिळवा"):
        if user_input:
            with st.spinner("AI विचार करत आहे..."):
                # System Prompt Logic
                system_prompt = f"You are the Abhyas Kranti Global AI Mentor. Answer the following topic in {selected_lang} with world-class depth and simplicity: {user_input}"
                
                # Database मध्ये नोंद करणे
                conn = sqlite3.connect('abhyas_kranti.db')
                conn.execute("INSERT INTO user_activity (topic, lang) VALUES (?, ?)", (user_input, selected_lang))
                conn.commit()
                conn.close()
                
                # दर्शवण्यासाठी मजकूर
                st.markdown(f"""
                <div style='background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #fbbf24;'>
                <strong>AI उत्तर:</strong><br><br>
                हे एक 'एआय मॉडेल' आहे. प्रत्यक्ष उत्तरासाठी तुमची OpenAI API Key 'Secrets' मध्ये जोडा.<br>
                विषय: {user_input}<br>
                भाषा: {selected_lang}
                </div>
                """, unsafe_allow_headers=True)
                st.balloons()
        else:
            st.warning("कृपया काहीतरी लिहा.")

elif section == "📚 अभ्यास साहित्य":
    st.subheader("📚 ई-पुस्तके आणि नोट्स")
    st.write("सर्व पुस्तके PDF स्वरूपात लवकरच उपलब्ध होतील.")

elif section == "📊 प्रगती":
    st.subheader("📊 तुमची शैक्षणिक प्रगती")
    try:
        conn = sqlite3.connect('abhyas_kranti.db')
        df = pd.read_sql_query("SELECT topic, lang, timestamp FROM user_activity ORDER BY timestamp DESC", conn)
        st.table(df)
        conn.close()
    except:
        st.write("अद्याप कोणतीही नोंद नाही.")

# ७. फुटर
st.markdown("<div class='footer'>© 2026 Abhyas Kranti | IIT Patna Capstone Project | Dr. Dnyaneshwar Gawalikar</div>", unsafe_allow_headers=True)
import streamlit as st

# १. जागतिक दर्जाचा लूक देण्यासाठी पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="अभ्यास क्रांती | AI Mentor",
    page_icon="📚",
    layout="wide" # स्क्रीनचा पूर्ण वापर करण्यासाठी
)

# २. मास्टर एआय प्रॉम्पट (System Instruction)
system_prompt = """
तुम्ही 'अभ्यास क्रांती' या जागतिक दर्जाच्या शैक्षणिक प्लॅटफॉर्मचे अधिकृत AI मार्गदर्शक आहात. 
तुमची कार्यपद्धती खालीलप्रमाणे असेल:

१. मल्टि-लँग्वेज सपोर्ट: वापरकर्त्याच्या भाषेत (मराठी/हिंदी/इंग्रजी) प्रतिसाद द्या. 
   मराठीत उत्तर देताना तांत्रिक शब्द कंसात इंग्रजीत लिहा (उदा. प्रकाशसंश्लेषण (Photosynthesis)).
२. स्ट्रक्चर्ड फॉरमॅट: उत्तरांमध्ये Bold मजकूर, Bullet Points आणि आवश्यक तिथे Tables चा वापर करा.
३. स्पर्धा परीक्षा फोकस: माहिती देताना ती MPSC, UPSC किंवा तत्सम परीक्षांच्या दृष्टीने महत्त्वाची कशी आहे, हे स्पष्ट करा.
४. संवाद: प्रत्येक उत्तराच्या शेवटी विद्यार्थ्याला विचार करायला लावणारा एक उपयोजनात्मक प्रश्न (Application-based question) विचारा.
५. व्हिज्युअल लूक: प्रतिसाद सुटसुटीत आणि वाचनीय असावा.
"""

# ३. इंटरफेस डिझाइन
st.title("🚀 अभ्यास क्रांती एआय मेंटॉर")
st.markdown("---")

# युजर इनपुट
user_input = st.chat_input("तुमचा अभ्यासाचा प्रश्न येथे विचारा...")

if user_input:
    # येथे तुमच्या एआय मॉडेलला (Gemini/OpenAI) कॉल जाईल
    # मॉडेलला पाठवताना: system_prompt + user_input असे पाठवावे.
    
    with st.chat_message("assistant"):
        st.write(f"येथे एआय 'अभ्यास क्रांती' च्या शैलीत उत्तर देईल...")
        # उदाहरण:
        # response = model.generate_content(system_prompt + user_input)
        # st.markdown(response.text)
# ही लिंक तुमच्या स्क्रीनशॉटवरून घेतलेली आहे
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/b2he5nnwn7i32bg6mangcu7kcccyma7d"
import streamlit as st
import requests

# १. तुमची वेबहुक लिंक येथे सेव्ह केली आहे
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/b2he5nnwn7i32bg6mangcu7kcccyma7d"

def ask_ai(question):
    # 'question' हा डेटा मेक.कॉमला पाठवण्यासाठी
    payload = {"question": question}
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        return response.text
    except Exception as e:
        return f"कनेक्शन एरर: {e}"

# ३. ॲपचा इंटरफेस
st.title("अभ्यास क्रांती AI")
user_query = st.text_input("तुमचा प्रश्न विचारा:")

if st.button("उत्तर मिळवा"):
    if user_query:
        answer = ask_ai(user_query)
        st.write(answer)
import streamlit as st
import requests

# निवडा बॉक्स (Sidebar/Selectbox)
choice = st.sidebar.selectbox("निवडा", ["होम", "AI मार्गदर्शक", "सराव परीक्षा", "निकाल"])

if choice == "AI मार्गदर्शक":
    st.title("🤖 AI मार्गदर्शक")
    
    # इथे इनपुट बॉक्स येईल
    user_question = st.text_input("तुमचा स्पर्धा परीक्षेचा प्रश्न विचारा:")
    
    if st.button("उत्तर मिळवा"):
        if user_question:
            # तुमच्या Make.com वेबहुकची लिंक इथे टाका
            webhook_url = "तुमची_वेबहुक_लिंक" 
            response = requests.post(webhook_url, json={"question": user_question})
            st.write(response.text)
        else:
            st.warning("कृपया प्रश्न टाईप करा.")
