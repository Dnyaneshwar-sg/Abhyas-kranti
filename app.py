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
    menu = ["होम", "सराव परीक्षा", "निकाल", "माहिती"]
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
