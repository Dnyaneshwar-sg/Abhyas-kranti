import google.generativeai as genai
import streamlit as st

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-pro"
)

def ask_ai(question):

    response = model.generate_content(
        question
    )

    return response.text
