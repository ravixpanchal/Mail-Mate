import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_email_response(email_text, tone, custom_note=""):
    extra = f"\nAdditional context or instruction: {custom_note}" if custom_note.strip() else ""

    prompt = f"""You are a professional email assistant. Write a polished, well-structured reply to the following email using a {tone.lower()} tone.

Guidelines:
- Be concise and clear
- Match the {tone.lower()} tone throughout
- Include a proper greeting and sign-off
- Do NOT include a subject line{extra}

Original Email:
{email_text}

Reply:"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text