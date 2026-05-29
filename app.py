import streamlit as st
from supabase import create_client, Client
from groq import Groq

# 1. ॲपची प्राथमिक मांडणी (Page Configuration)
st.set_page_config(page_title="अभ्यास क्रांती AI", page_icon="📚", layout="centered")

# --- साईडबार (Sidebar) मधील फीचर्स ---
st.sidebar.title("⚙️ नियंत्रण पॅनेल")
# चॅट हिस्ट्री रिसेट करण्यासाठी बटण
if st.sidebar.button("🧹 चॅट इतिहास पुसा (Clear Chat)"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **अभ्यास क्रांती AI** - विद्यार्थ्यांच्या शंकांचे सोपे आणि अचूक निरसन करण्यासाठी तयार केलेले खास ॲप.")

# मुख्य स्क्रीनची शीर्षके
st.title("📚 अभ्यास क्रांती AI")
st.subheader("विद्यार्थ्यांच्या शंकांचे सोपे निरसन!")

# 2. Streamlit Secrets मधून कीज (Keys) मिळवणे आणि क्लायंट सुरू करणे
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    
    # क्लायंट ऑब्जेक्ट्स तयार करणे
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as init_err:
    st.error(f"सेटिंग्ज/Secrets मध्ये त्रुटी आहे: {init_err}")
    st.info("कृपया Streamlit Cloud मधील Secrets नीट सेट केल्याची खात्री करा.")

# 3. चॅट हिस्ट्री (Chat History) सुरू करणे
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. जुना संवाद स्क्रीनवर दाखवणे
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. विद्यार्थ्याकडून प्रश्न स्वीकारणे (Chat Input)
if query := st.chat_input("तुमचा शैक्षणिक प्रश्न इथे टाईप करा..."):
    
    # विद्यार्थ्याचा प्रश्न स्क्रीनवर दाखवणे
    with st.chat_message("user"):
        st.write(query)
        
    # 6. Groq AI कडून उत्तर मिळवणे
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # तुमचा मॉडेल आयडी
            messages=[
                {"role": "system", "content": "तुम्ही 'अभ्यास क्रांती' ॲपचे तज्ज्ञ मार्गदर्शक आहात. विद्यार्थ्यांच्या प्रश्नांची उत्तरे मराठीत, सोप्या आणि शुद्ध भाषेत द्या."},
                *st.session_state.chat_history,
                {"role": "user", "content": query}
            ]
        )
        ai_response = completion.choices[0].message.content
    except Exception as ai_err:
        ai_response = f"क्षमस्व, उत्तर तयार करताना तांत्रिक अडचण आली: {ai_err}"

    # AI चे उत्तर स्क्रीनवर दाखवणे
    with st.chat_message("assistant"):
        st.write(ai_response)

    # 7. चॅट हिस्ट्री अपडेट करणे
    st.session_state.chat_history.append({"role": "user", "content": query})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    # 8. सुपाबेस डेटाबेसमध्ये सुरक्षित बॅकअप नोंदवणे (Safe Database Block)
    try:
        data = {
            "query": query,
            "response": ai_response
        }
        # सुपाबेसमध्ये डेटा सुरक्षित सेव्ह करणे
        supabase.table("search_history").insert(data).execute()
    except Exception as db_err:
        # डेटाबेसमध्ये टेबल किंवा कॉलम जुळला नाही तरी ॲप क्रॅश होणार नाही
        st.caption("ℹ️ डेटाबेस बॅकअप नोंदवला गेला नाही, पण ॲप कार्यरत आहे.")

    # स्क्रीन रिफ्रेश करणे
    st.rerun()
