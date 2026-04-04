import streamlit as st
from agents.email_agent import generate_email_response
from utils.email_sender import send_email

st.set_page_config(
    page_title="Reply Nexa – AI Email Responder",
    page_icon="✉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:       #0A0C14;
    --surface:  #0D1208;
    --surface2: #111A0E;
    --border:   #1A2414;
    --border2:  #1E2E18;
    --accent:   #22C55E;
    --accent2:  #4ADE80;
    --accent3:  #86EFAC;
    --text:     #E8F5E9;
    --muted:    #5A7A5E;
    --radius:   12px;
    --radius-sm:8px;
}

/* ── Global ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
* { box-sizing: border-box; }

/* grid overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(34,197,94,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34,197,94,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Layout ── */
[data-testid="block-container"] {
    max-width: 780px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    position: relative;
    z-index: 1;
}
@media (max-width: 600px) {
    [data-testid="block-container"] { padding: 1rem 0.75rem 3rem; }
}

/* ── Hero ── */
.mm-hero {
    text-align: center;
    padding: 3rem 1rem 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.mm-topbadge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 99px;
    padding: 6px 18px 6px 8px;
    margin-bottom: 1.75rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #86EFAC;
}
.mm-topbadge .dot {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, var(--accent), #16A34A);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    box-shadow: 0 0 12px rgba(34,197,94,0.5);
}
.mm-topbadge .live {
    width: 6px; height: 6px;
    background: var(--accent2);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--accent2);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.3; }
}

/* ── FIXED: Hero title — single line, horizontally centered ── */
.mm-hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 16vw, 8rem);
    font-weight: 400;
    letter-spacing: 0.04em;
    line-height: 1;
    margin: 0 0 0.3rem;
    color: var(--text);
    white-space: nowrap;
    text-align: center;
    width: 100%;
}
.mm-hero-title .grad {
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.mm-underline {
    width: 100%;
    max-width: 420px;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 0.6rem auto 1.25rem;
    border-radius: 99px;
}
.mm-hero p {
    color: var(--muted);
    font-size: clamp(0.85rem, 2.5vw, 1rem);
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.01em;
    text-align: center;
}

/* ── Responsive columns ── */
@media (max-width: 600px) {
    [data-testid="stColumns"] {
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
    [data-testid="stColumns"] > div {
        width: 100% !important;
        min-width: 100% !important;
    }
    .mm-hero-title {
        font-size: clamp(3rem, 18vw, 5rem);
        white-space: normal;
        word-break: break-word;
    }
}

/* ── Widget labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #6B7280 !important;
}

/* ── Inputs & Textareas ── */
textarea,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
[data-baseweb="textarea"] textarea,
[data-baseweb="input"] input {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    line-height: 1.7 !important;
    color: #A7F3C0 !important;
    -webkit-text-fill-color: #A7F3C0 !important;
    background: linear-gradient(160deg, #071510 0%, #0A1C0F 60%, #061210 100%) !important;
    border: 1px solid rgba(34,197,94,0.35) !important;
    border-radius: 10px !important;
    caret-color: var(--accent2) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
    box-shadow:
        0 0 0 1px rgba(34,197,94,0.08) inset,
        0 2px 12px rgba(0,0,0,0.5),
        0 0 24px rgba(34,197,94,0.04) !important;
}

/* Glowing left accent bar on the textarea wrapper */
.stTextArea > div {
    border-left: 2px solid rgba(34,197,94,0.4) !important;
    border-radius: 10px !important;
    padding-left: 0 !important;
    box-shadow: -4px 0 18px rgba(34,197,94,0.08) !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextArea > div:focus-within {
    border-left-color: var(--accent) !important;
    box-shadow: -6px 0 28px rgba(34,197,94,0.2) !important;
}

/* Placeholder */
textarea::placeholder,
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-baseweb="textarea"] textarea::placeholder,
[data-baseweb="input"] input::placeholder {
    color: rgba(34,197,94,0.22) !important;
    -webkit-text-fill-color: rgba(34,197,94,0.22) !important;
    font-style: italic !important;
}

/* Focus state — vivid green glow */
textarea:focus,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    background: linear-gradient(160deg, #081a12 0%, #0D2416 60%, #081510 100%) !important;
    box-shadow:
        0 0 0 3px rgba(34,197,94,0.12) inset,
        0 0 0 2px rgba(34,197,94,0.18),
        0 0 32px rgba(34,197,94,0.15),
        0 0 64px rgba(34,197,94,0.06) !important;
    outline: none !important;
    color: #DCFCE7 !important;
    -webkit-text-fill-color: #DCFCE7 !important;
}

/* ── Kill Streamlit/BaseWeb red focus ring on ALL wrapper containers ── */
[data-baseweb="textarea"],
[data-baseweb="input"],
[data-baseweb="base-input"],
[data-baseweb="textarea"] > div,
[data-baseweb="input"] > div,
[data-baseweb="base-input"] > div,
.stTextArea > div > div,
.stTextInput > div > div,
[data-testid="stTextArea"] > div,
[data-testid="stTextInput"] > div {
    border-color: rgba(34,197,94,0.35) !important;
    outline: none !important;
    box-shadow: none !important;
}
[data-baseweb="textarea"]:focus-within,
[data-baseweb="input"]:focus-within,
[data-baseweb="base-input"]:focus-within,
[data-baseweb="textarea"] > div:focus-within,
[data-baseweb="input"] > div:focus-within,
[data-baseweb="base-input"] > div:focus-within,
.stTextArea > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--accent) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(34,197,94,0.18), 0 0 32px rgba(34,197,94,0.12) !important;
}
/* Nuclear option — catch any remaining Streamlit red ring */
*:focus, *:focus-visible, *:focus-within {
    outline-color: var(--accent) !important;
}
textarea:focus-visible,
input:focus-visible {
    outline: none !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border2) !important;
    background: var(--surface2) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
}
[data-baseweb="menu"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
}
[data-baseweb="menu"] li {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text) !important;
    background: var(--surface2) !important;
}
[data-baseweb="menu"] li:hover {
    background: rgba(34,197,94,0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, #16A34A 100%);
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1.5rem;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    cursor: pointer;
    letter-spacing: 0.03em;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 24px rgba(34,197,94,0.3);
    text-transform: uppercase;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(34,197,94,0.45);
}
.stButton > button:active { transform: translateY(0); }

/* ── Section label ── */
.mm-section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 0.6rem;
    margin-top: 0.25rem;
}

/* ── Divider ── */
.mm-divider {
    border: none;
    border-top: 1px solid var(--border2);
    margin: 2rem 0 1.5rem;
}

/* ── Footer ── */
.mm-footer {
    text-align: center;
    color: #2D5A33;
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border);
    font-weight: 500;
    letter-spacing: 0.03em;
}
.mm-footer strong { color: var(--accent); font-weight: 700; }

/* ── Streamlit chrome overrides ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    background: rgba(34,197,94,0.08) !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
}
[data-testid="stSpinner"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--muted) !important;
}
[data-testid="stCaptionContainer"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: #2D5A33 !important;
}
[data-testid="stCode"] { border-radius: var(--radius-sm) !important; }

div[data-testid="stAlert"] p { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mm-hero">
    <div class="mm-topbadge">
        <div class="dot">✦</div>
        <span>AI Email</span>
        &nbsp;·&nbsp;
        <span>Gemini</span>
        &nbsp;·&nbsp;
        <span>2026</span>
        <div class="live"></div>
    </div>
    <div class="mm-hero-title">
        REPLY&nbsp;<span class="grad">NEXA</span>
    </div>
    <div class="mm-underline"></div>
    <p>Paste an email &nbsp;·&nbsp; pick a tone &nbsp;·&nbsp; choose a language &nbsp;·&nbsp; get a polished reply</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""
if "last_tone" not in st.session_state:
    st.session_state.last_tone = ""
if "last_language" not in st.session_state:
    st.session_state.last_language = ""

# ── Language options ───────────────────────────────────────────────────────────
LANGUAGES = [
    "English", "Hindi", "Spanish", "French", "German",
    "Portuguese", "Arabic", "Japanese", "Chinese (Simplified)",
    "Korean", "Italian", "Russian", "Bengali", "Gujarati",
    "Marathi", "Tamil", "Telugu", "Kannada", "Punjabi",
    "Dutch", "Polish", "Turkish", "Vietnamese", "Thai",
]

# ── Inputs ─────────────────────────────────────────────────────────────────────
with st.container():
    email_text = st.text_area(
        label="Original Email",
        placeholder="Paste the email you received here…",
        height=200,
        key="email_input"
    )

    # Row 1: Tone + Language
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        tone = st.selectbox(
            label="Tone",
            options=["Professional", "Friendly", "Apologetic", "Persuasive", "Concise"],
            key="tone_select"
        )
    with col2:
        language = st.selectbox(
            label="Reply Language",
            options=LANGUAGES,
            key="language_select",
            help="The generated reply will be written in this language."
        )

    # Row 2: Recipient email (full width)
    recipient_email = st.text_input(
        label="Recipient Email",
        placeholder="recipient@example.com",
        key="recipient_input"
    )

    custom_note = st.text_input(
        label="Extra Instructions (optional)",
        placeholder="e.g. Follow up by Friday, keep it under 100 words…",
        key="custom_note"
    )

# ── Generate ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
generate_clicked = st.button("⚡  GENERATE REPLY", use_container_width=True)

if generate_clicked:
    if not email_text.strip():
        st.warning("Please paste the email content first.")
    else:
        with st.spinner("Drafting your reply…"):
            try:
                result = generate_email_response(
                    email_text, tone, custom_note, language
                )
                st.session_state.generated_response = result
                st.session_state.last_tone = tone
                st.session_state.last_language = language
            except Exception as e:
                st.error(f"Generation failed: {e}")

# ── Output ─────────────────────────────────────────────────────────────────────
if st.session_state.generated_response:
    st.markdown('<hr class="mm-divider">', unsafe_allow_html=True)

    lang_tag = f" · {st.session_state.last_language}" if st.session_state.last_language else ""
    edited_response = st.text_area(
        label=f"Generated Reply  [{st.session_state.last_tone}{lang_tag}]",
        value=st.session_state.generated_response,
        height=280,
        key="edit_response",
        help="Edit the reply before sending."
    )
    st.caption("You can edit the reply above before sending.")

    col_copy, col_send = st.columns([1, 1], gap="small")
    with col_copy:
        if st.button("COPY TO CLIPBOARD", use_container_width=True):
            st.code(edited_response, language="")
            st.info("Select the text above and copy (Ctrl+C / Cmd+C)")

    with col_send:
        send_clicked = st.button("SEND EMAIL", use_container_width=True)
        if send_clicked:
            if not recipient_email.strip():
                st.warning("Enter a recipient email before sending.")
            else:
                with st.spinner(f"Sending to {recipient_email}…"):
                    status = send_email(recipient_email, edited_response)
                    if status:
                        st.success(f"Email sent to {recipient_email}!")
                    else:
                        st.error("Sending failed. Check your SMTP secrets.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mm-footer">
    Made with ❤️ by <strong>Ravi Panchal</strong> &nbsp;·&nbsp; All Rights Reserved © 2026
</div>
""", unsafe_allow_html=True)