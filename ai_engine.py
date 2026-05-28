import google.generativeai as genai
import streamlit as st

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-1.5_pro"
)

def ask_ai(question):

    try:

        response = model.generate_content(question)

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"
