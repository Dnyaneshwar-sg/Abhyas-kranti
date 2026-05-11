
import streamlit as st
import requests
import sqlite3
import pandas as pd
from datetime import date

# १. डेटाबेस सेटअप (ऑफलाइन प्रगती साठवण्यासाठी)
def init_db():
    conn = sqlite3.connect('abhyas_kranti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress 
                 (date TEXT, subject TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# २. मुख्य ॲप डिझाइन
def main():
    st.set_page_config(page_title="अभ्यास क्रांती", page_icon="🎓", layout="wide")
    
    # CSS फॉर ग्रामीण भाग (Low Data Usage & Clean Look)
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
        </style>
        """, unsafe_allow_html=True)

    st.title("🎓 अभ्यास क्रांती")
    st.subheader("ग्रामीण भागातील विद्यार्थ्यांसाठी मोफत डिजिटल व्यासपीठ")

    # ३. साइडबार मेनू
    menu = ["🏠 होम", "🤖 AI मार्गदर्शक", "📚 शालेय शिक्षण (१ली-१२वी)", "🏆 स्पर्धा परीक्षा (MPSC/UPSC)", "🎖️ संरक्षण दल (Army/Navy/Air Force)", "🧬 NEET/JEE/NDA", "📊 माझा स्टडी प्लॅन"]
    choice = st.sidebar.selectbox("विभाग निवडा", menu)

    init_db()

    # --- विभाग १: होम ---
    if choice == "🏠 होम":
        st.write("### स्वागत आहे विद्यार्थी मित्रांनो!")
        st.info("हे ॲप विशेषतः ग्रामीण भागातील गरीब आणि होतकरू विद्यार्थ्यांसाठी बनवले आहे. इथे तुम्हाला सर्व शिक्षण मोफत मिळेल.")
        st.image("https://img.icons8.com/clouds/200/education.png")
        st.write("#### उपलब्ध सुविधा:")
        st.write("* १ ली ते PhD पर्यंतचे मार्गदर्शन\n* सर्व स्पर्धा परीक्षांच्या नोट्स\n* २४/७ AI मार्गदर्शक मदत")

    # --- विभाग २: AI मार्गदर्शक (Make.com Integration) ---
    elif choice == "🤖 AI मार्गदर्शक":
        st.header("🤖 AI मार्गदर्शक (Multi-language)")
        st.write("तुमचा प्रश्न मराठी, हिंदी किंवा इंग्रजीमध्ये विचारा.")
       " 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"
        user_input = st.text_input("तुमचा प्रश्न इथे टाईप करा:", placeholder="उदा. स्कॉलरशिप परीक्षेची तयारी कशी करू?")
        
        if st.button("उत्तर मिळवा"):
            if user_input:
                with st.spinner('AI विचार करत आहे...'):
                    # --- तुमची MAKE.COM WEBHOOK LINK इथे पेस्ट करा ---
                    webhook_url “https://hook.eu2.make.com/ece4xd8coueyvk75ao8g9behgp7dfsbe"
                    
                        payload = {"question": user_input}
                        response = requests.post(webhook_url, json=payload)
                        
                        if response.status_code == 200:
                            st.success("उत्तर:")
                            st.write(response.text)
                        else:
                            st.error("Make.com शी संपर्क होऊ शकला नाही. कृपया लिंक तपासा.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("कृपया प्रश्न टाईप करा.")

    # --- विभाग ३: परीक्षा विभाग (नमुना नोट्स) ---
    elif choice in ["📚 शालेय शिक्षण (१ली-१२वी)", "🏆 स्पर्धा परीक्षा (MPSC/UPSC)", "🎖️ संरक्षण दल (Army/Navy/Air Force)"]:
        st.header(f"📖 {choice}")
        st.write("येथे तुम्हाला मोफत नोट्स आणि सराव पेपर्स मिळतील.")
        
        # ऑफलाइन साठवण्यासाठी कॅश मेमरी वापर
        @st.cache_data
        def get_notes():
            return "महत्त्वाच्या नोट्स: १. परीक्षेचा अभ्यासक्रम समजून घ्या. २. रोज सराव करा. ३. मागील वर्षाचे पेपर सोडवा."
        
        st.info(get_notes())
        st.button("नोट्स PDF डाउनलोड करा (ऑफलाइन वापरासाठी)")

    # --- विभाग ४: स्टडी प्लॅन (Database use) ---
    elif choice == "📊 माझा स्टडी प्लॅन":
        st.header("📅 माझा स्टडी प्लॅन")
        sub = st.text_input("विषयाचे नाव:")
        stat = st.selectbox("स्थिती", ["सुरू करायचे आहे", "अभ्यास चालू आहे", "पूर्ण झाले"])
        
        if st.button("प्लॅन सेव्ह करा"):
            conn = sqlite3.connect('abhyas_kranti.db')
            c = conn.cursor()
            c.execute("INSERT INTO progress VALUES (?, ?, ?)", (date.today(), sub, stat))
            conn.commit()
            st.success("तुमची प्रगती सेव्ह झाली आहे (ऑफलाइन उपलब्ध)!")
            
        st.write("### माझी प्रगती")
        conn = sqlite3.connect('abhyas_kranti.db')
        df = pd.read_sql_query("SELECT * FROM progress", conn)
        st.table(df)
https://hook.eu2.make.com/ece4xd8coueyvk75ao8g9behgp7dfsbe
if __name__ == '__main__':
    main()
