import streamlit as st
from agents.email_agent import generate_email_response
from utils.email_sender import send_email

st.set_page_config(
    page_title="MailMate – AI Email Responder",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg: #F0F4FF;
    --surface: #FFFFFF;
    --surface2: #F7F9FF;
    --accent: #4361EE;
    --accent2: #7209B7;
    --accent-light: #EEF2FF;
    --border: #D8E0F0;
    --text: #0D1B2A;
    --muted: #64748B;
    --success: #06D6A0;
    --warn: #FFB703;
    --radius: 14px;
    --radius-sm: 8px;
    --shadow: 0 4px 24px rgba(67,97,238,0.10);
    --shadow-hover: 0 8px 32px rgba(67,97,238,0.18);
}

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
* { box-sizing: border-box; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Layout ── */
[data-testid="block-container"] {
    max-width: 760px;
    margin: 0 auto;
    padding: 2rem 1.25rem 3rem;
}
@media (max-width: 600px) {
    [data-testid="block-container"] { padding: 1rem 0.75rem 2rem; }
}

/* ── Hero ── */
.mm-hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
}
.mm-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-light);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 99px;
    border: 1px solid #C7D4FF;
    margin-bottom: 1rem;
}
.mm-hero h1 {
    font-size: clamp(2rem, 6vw, 3rem);
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.04em;
    margin: 0 0 0.4rem;
    line-height: 1.1;
}
.mm-hero h1 span {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.mm-hero p {
    color: var(--muted);
    font-size: 1.02rem;
    margin: 0;
    font-weight: 500;
}

/* ── Card ── */
.mm-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s;
}
.mm-card:hover { box-shadow: var(--shadow-hover); }
@media (max-width: 480px) { .mm-card { padding: 1.1rem; } }

/* ── Section labels ── */
.mm-label {
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--muted);
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

/* ── Textarea & inputs — THE FIX ── */
/* Force visible text in ALL Streamlit input elements */
textarea,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
[data-baseweb="textarea"] textarea,
[data-baseweb="input"] input {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.875rem !important;
    color: #0D1B2A !important;          /* ← dark text, always visible */
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    caret-color: var(--accent) !important;
    -webkit-text-fill-color: #0D1B2A !important; /* Safari / Webkit fix */
}
textarea::placeholder,
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-baseweb="textarea"] textarea::placeholder,
[data-baseweb="input"] input::placeholder {
    color: #A0AABA !important;
    -webkit-text-fill-color: #A0AABA !important;
}
textarea:focus,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(67,97,238,0.13) !important;
    outline: none !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface2) !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
}
[data-baseweb="select"] [data-testid="stSelectbox"] {
    color: var(--text) !important;
}
/* Dropdown option text */
[data-baseweb="menu"] li {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text) !important;
}

/* ── Primary button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.97rem !important;
    padding: 0.8rem 1.5rem;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer;
    letter-spacing: 0.01em;
    transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s;
    box-shadow: 0 4px 18px rgba(67,97,238,0.28);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(67,97,238,0.38);
    opacity: 0.96;
}
.stButton > button:active { transform: translateY(0); }

/* ── Response output ── */
.mm-response {
    background: #F0F5FF;
    border: 1.5px solid #C7D9FF;
    border-left: 4px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.875rem;
    line-height: 1.75;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Divider ── */
.mm-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Status badges ── */
.mm-chip {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 99px;
    background: var(--accent-light);
    color: var(--accent);
    border: 1px solid #C7D4FF;
    margin-left: 6px;
    vertical-align: middle;
    letter-spacing: 0.04em;
}

/* ── Footer ── */
.mm-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 0.78rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-weight: 500;
}
.mm-footer strong {
    color: var(--accent);
    font-weight: 700;
}

/* ── Streamlit alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--muted) !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
}

/* ── Code block (copy workaround) ── */
[data-testid="stCode"] {
    border-radius: var(--radius-sm) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mm-hero">
    <div class="mm-badge">✨ Powered by Gemini 1.5 Flash</div>
    <h1>📧 <span>MailMate</span></h1>
    <p>Paste an email · pick a tone · get a polished reply in seconds</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""
if "last_tone" not in st.session_state:
    st.session_state.last_tone = ""

# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="mm-card">', unsafe_allow_html=True)

st.markdown('<div class="mm-label">📨 Original Email</div>', unsafe_allow_html=True)
email_text = st.text_area(
    label="email_input",
    label_visibility="collapsed",
    placeholder="Paste the email you received here…",
    height=190,
    key="email_input"
)

col1, col2 = st.columns([1, 1], gap="medium")
with col1:
    st.markdown('<div class="mm-label" style="margin-top:0.75rem">🎭 Tone</div>', unsafe_allow_html=True)
    tone = st.selectbox(
        label="tone_select",
        label_visibility="collapsed",
        options=["Professional", "Friendly", "Apologetic", "Persuasive", "Concise"],
        key="tone_select"
    )
with col2:
    st.markdown('<div class="mm-label" style="margin-top:0.75rem">📬 Recipient Email</div>', unsafe_allow_html=True)
    recipient_email = st.text_input(
        label="recipient_input",
        label_visibility="collapsed",
        placeholder="recipient@example.com",
        key="recipient_input"
    )

st.markdown('<div class="mm-label" style="margin-top:0.75rem">💬 Extra Instructions <span style="font-weight:400;text-transform:none;font-size:0.78rem">(optional)</span></div>', unsafe_allow_html=True)
custom_note = st.text_input(
    label="custom_note",
    label_visibility="collapsed",
    placeholder="e.g. Mention we'll follow up by Friday, keep it under 100 words…",
    key="custom_note"
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Generate button ────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:0.25rem'></div>", unsafe_allow_html=True)
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
    st.markdown('<hr class="mm-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="mm-label">✉️ Generated Reply '
        f'<span class="mm-chip">{st.session_state.last_tone}</span></div>',
        unsafe_allow_html=True
    )

    edited_response = st.text_area(
        label="edit_response",
        label_visibility="collapsed",
        value=st.session_state.generated_response,
        height=270,
        key="edit_response",
        help="You can edit the reply before sending."
    )
    st.caption("✏️ Feel free to edit the reply above before sending.")

    col_copy, col_send = st.columns([1, 1], gap="small")

    with col_copy:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.code(edited_response, language="")
            st.info("Select the text above and copy (Ctrl+C / Cmd+C)")

    with col_send:
        send_clicked = st.button("🚀 Send Email", use_container_width=True)
        if send_clicked:
            if not recipient_email.strip():
                st.warning("⚠️ Enter a recipient email before sending.")
            else:
                with st.spinner(f"Sending to {recipient_email}…"):
                    status = send_email(recipient_email, edited_response)
                    if status:
                        st.success(f"✅ Email sent to **{recipient_email}**!")
                    else:
                        st.error("❌ Sending failed. Check your SMTP secrets.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mm-footer">
    Made with ❤️ by <strong>Ravi Panchal</strong> &nbsp;·&nbsp; All Rights Reserved © 2026
</div>
""", unsafe_allow_html=True)