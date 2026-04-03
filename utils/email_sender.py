import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, body, subject="Re: Your Email"):
    try:
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["EMAIL_PASSWORD"]
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        st.error(f"SMTP Error: {e}")
        return False