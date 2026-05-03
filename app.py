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
