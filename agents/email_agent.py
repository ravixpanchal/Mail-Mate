import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Free-tier model priority: highest quota first → fallback chain
FREE_TIER_MODELS = [
    "gemini-2.5-flash-lite",        # 1,000 req/day — best free option
    "gemini-2.5-flash",             # 250 req/day
    "gemini-2.0-flash-lite",        # fallback
    "gemini-2.0-flash",             # last resort
]

def generate_email_response(email_text: str, tone: str, custom_note: str = "") -> str:
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

    last_error = None
    for model_name in FREE_TIER_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_str = str(e)
            # Only skip to next model on quota / not-found errors
            if any(code in err_str for code in ["429", "404", "quota", "not found", "not supported"]):
                last_error = e
                continue
            # For any other error, raise immediately
            raise e

    # All models exhausted
    raise Exception(
        f"All free-tier models are currently quota-limited. "
        f"Please wait a few minutes and try again, or check your quota at "
        f"https://aistudio.google.com/. Last error: {last_error}"
    )