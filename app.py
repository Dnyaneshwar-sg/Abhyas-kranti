import streamlit as st
from ai_engine import ask_ai

st.set_page_config(
    page_title="Abhyas Kranti",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Abhyas Kranti AI")

st.subheader(
    "AI Powered Educational Ecosystem"
)

question = st.text_input(
    "Ask your question"
)

if st.button("Generate Answer"):

    if question:

        with st.spinner("Generating Answer..."):

            answer = ask_ai(question)

            st.success(answer)

    else:

        st.warning(
            "Please enter a question"
        )
