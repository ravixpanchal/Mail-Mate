import streamlit as st
from agents.email_agent import generate_email_response
from utils.email_sender import send_email

st.set_page_config(
    page_title="MailMate – AI Email Responder",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Responsive custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --accent: #4F8EF7;
    --accent-dark: #2563EB;
    --surface: #F8FAFF;
    --border: #DDE3F0;
    --text: #1A1F36;
    --muted: #6B7280;
    --success: #10B981;
    --radius: 12px;
}

/* Global */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Sora', sans-serif;
    background-color: var(--surface);
    color: var(--text);
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main container width clamp for all screens */
[data-testid="block-container"] {
    max-width: 780px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
}

/* Hero header */
.mailmate-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    margin-bottom: 1.5rem;
}
.mailmate-header h1 {
    font-size: clamp(1.8rem, 5vw, 2.6rem);
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.03em;
    margin: 0;
}
.mailmate-header p {
    color: var(--muted);
    font-size: 1rem;
    margin-top: 0.4rem;
}
.badge {
    display: inline-block;
    background: #EEF4FF;
    color: var(--accent-dark);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    margin-bottom: 0.75rem;
    letter-spacing: 0.05em;
}

/* Card wrapper */
.card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Section labels */
.section-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* Textareas & inputs */
textarea, .stTextInput input, .stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    background: #FAFBFF !important;
}
textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.12) !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border-color: var(--border) !important;
}

/* Primary button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
    color: white;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79,142,247,0.35);
}
.stButton > button:active {
    transform: translateY(0);
}

/* Response output box */
.response-box {
    background: #F0F5FF;
    border: 1px solid #C7D9FF;
    border-left: 4px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}

/* Action row */
.action-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

/* Tone pills */
.tone-info {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.tone-pill {
    font-size: 0.75rem;
    padding: 3px 10px;
    border-radius: 99px;
    border: 1px solid var(--border);
    color: var(--muted);
}

/* Divider */
hr.slim {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.25rem 0;
}

/* Mobile tweaks */
@media (max-width: 480px) {
    [data-testid="block-container"] { padding: 0.75rem 0.5rem; }
    .card { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mailmate-header">
    <div class="badge">✨ Powered by Gemini 1.5 Flash</div>
    <h1>📧 MailMate</h1>
    <p>Paste an email → pick a tone → get a polished reply in seconds</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""
if "last_tone" not in st.session_state:
    st.session_state.last_tone = ""

# ── Input card ─────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">📨 Original Email</div>', unsafe_allow_html=True)
    email_text = st.text_area(
        label="email_input",
        label_visibility="collapsed",
        placeholder="Paste the email you received here…",
        height=180,
        key="email_input"
    )

    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.markdown('<div class="section-label">🎭 Tone</div>', unsafe_allow_html=True)
        tone = st.selectbox(
            label="tone_select",
            label_visibility="collapsed",
            options=["Professional", "Friendly", "Apologetic", "Persuasive", "Concise"],
            key="tone_select"
        )
    with col2:
        st.markdown('<div class="section-label">📬 Recipient Email</div>', unsafe_allow_html=True)
        recipient_email = st.text_input(
            label="recipient_input",
            label_visibility="collapsed",
            placeholder="recipient@example.com",
            key="recipient_input"
        )

    st.markdown('<div class="section-label" style="margin-top:0.75rem">💬 Extra Instructions <span style="font-weight:400;text-transform:none">(optional)</span></div>', unsafe_allow_html=True)
    custom_note = st.text_input(
        label="custom_note",
        label_visibility="collapsed",
        placeholder="e.g. Mention we'll follow up by Friday, keep it under 100 words…",
        key="custom_note"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ── Generate button ────────────────────────────────────────────────────────────
generate_clicked = st.button("⚡ Generate Reply", use_container_width=True)

if generate_clicked:
    if not email_text.strip():
        st.warning("⚠️ Please paste the email content first.")
    else:
        with st.spinner("Gemini is drafting your reply…"):
            try:
                result = generate_email_response(email_text, tone, custom_note)
                st.session_state.generated_response = result
                st.session_state.last_tone = tone
            except Exception as e:
                st.error(f"Generation failed: {e}")

# ── Output card ────────────────────────────────────────────────────────────────
if st.session_state.generated_response:
    st.markdown("---")
    st.markdown(f'<div class="section-label">✉️ Generated Reply &nbsp;<span style="font-weight:400;text-transform:none;color:#4F8EF7">[{st.session_state.last_tone}]</span></div>', unsafe_allow_html=True)

    # Editable response
    edited_response = st.text_area(
        label="edit_response",
        label_visibility="collapsed",
        value=st.session_state.generated_response,
        height=260,
        key="edit_response",
        help="You can edit the reply before sending."
    )
    st.caption("✏️ Edit the reply above before sending if needed.")

    col_copy, col_send = st.columns([1, 1], gap="small")

    with col_copy:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.code(edited_response, language="")
            st.info("Select the text above and copy (Ctrl+C / Cmd+C)")

    with col_send:
        send_clicked = st.button("🚀 Send Email", use_container_width=True)
        if send_clicked:
            if not recipient_email.strip():
                st.warning("⚠️ Enter recipient email before sending.")
            else:
                with st.spinner(f"Sending to {recipient_email}…"):
                    status = send_email(recipient_email, edited_response)
                    if status:
                        st.success(f"✅ Email sent to **{recipient_email}**!")
                    else:
                        st.error("❌ Sending failed. Check your SMTP secrets.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="slim">
<p style="text-align:center;color:#9CA3AF;font-size:0.78rem;margin-top:0.5rem">
    MailMate · Built with Streamlit & Gemini 1.5 Flash · Free API tier
</p>
""", unsafe_allow_html=True)