import streamlit as st
import sqlite3
import pandas as pd

# डेटाबेस सेटअप
def init_db():
    conn = sqlite3.connect('abhyas_kranti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (name TEXT, score INTEGER, total INTEGER)''')
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="अभ्यास क्रांती", page_icon="📚")
    st.title("📚 अभ्यास क्रांती")
    st.subheader("स्पर्धा परीक्षा तयारी केंद्र")

    menu = ["होम", "सराव परीक्षा", "निकाल", "माहिती"]
    choice = st.sidebar.selectbox("निवडा", menu)

    init_db()

    if choice == "होम":
        st.write("### स्वागत आहे!")
        st.info("तुमच्या स्पर्धा परीक्षेच्या तयारीसाठी हे एक उत्तम व्यासपीठ आहे.")
        
    elif choice == "सराव परीक्षा":
        st.write("### सामान्य ज्ञान सराव")
        with st.form(key='quiz_form'):
            q1 = st.radio("१. महाराष्ट्राची राजधानी कोणती?", ("पुणे", "मुंबई", "नागपूर", "छत्रपती संभाजीनगर"))
            submit_button = st.form_submit_button(label='निकाल पहा')
            
            if submit_button:
                score = 1 if q1 == "मुंबई" else 0
                st.success(f"तुमचा स्कोर: {score}/1")
                
                # निकाल जतन करणे
                conn = sqlite3.connect('abhyas_kranti.db')
                c = conn.cursor()
                c.execute("INSERT INTO results (name, score, total) VALUES (?, ?, ?)", ("विद्यार्थी", score, 1))
                conn.commit()
                conn.close()

    elif choice == "निकाल":
        st.write("### मागील निकाल")
        conn = sqlite3.connect('abhyas_kranti.db')
        try:
            df = pd.read_sql_query("SELECT * FROM results", conn)
            st.dataframe(df)
        except:
            st.warning("अद्याप निकाल नाहीत.")
        finally:
            conn.close()

    # फुटर माहिती
    st.sidebar.markdown("---")
    st.sidebar.write("© 2026 Abhyas Kranti | IIT Patna")
    st.sidebar.write("Capstone Project | Dr. Dnyaneshwar Gawalikar")

if __name__ == '__main__':
    main()
