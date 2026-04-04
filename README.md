# Reply Nexa ✉️

> **AI-powered email reply generator** — paste an email, pick your tone and language, get a polished reply in seconds.

Built with **Streamlit** + **Google Gemini API**, featuring real SMTP email sending and multi-language support.

---

## ✨ Features

- **AI Reply Generation** — Gemini drafts context-aware, professional replies to any email
- **5 Tone Modes** — Professional · Friendly · Apologetic · Persuasive · Concise
- **24+ Language Support** — Generate replies in English, Hindi, Spanish, French, Arabic, Japanese, and more
- **Edit Before Send** — Review and tweak the AI reply before it goes out
- **One-Click Send** — Built-in SMTP integration to send directly from the app
- **Free-Tier Smart Fallback** — Automatically cycles through Gemini models to stay within quota limits
- **Fully Responsive UI** — Dark cyberpunk theme with green accent, works on desktop & mobile

---

## 🗂️ Project Structure

```
reply-nexa/
├── main.py                  # Streamlit app entry point
├── requirements.txt         # Python dependencies
├── agents/
│   └── email_agent.py       # Gemini AI reply generation logic
└── utils/
    └── email_sender.py      # SMTP email sending utility
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reply-nexa.git
cd reply-nexa
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-google-gemini-api-key"
SENDER_EMAIL   = "your-gmail@gmail.com"
EMAIL_PASSWORD = "your-gmail-app-password"

# Optional — defaults shown
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
```

> **Gmail users:** Generate an [App Password](https://myaccount.google.com/apppasswords) (requires 2FA enabled). Do **not** use your regular Gmail password.

### 4. Run the app

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key into your `secrets.toml`

The app uses free-tier Gemini models with automatic fallback:

| Model | Daily Quota |
|---|---|
| `gemini-2.5-flash-lite` | 1,000 req/day (primary) |
| `gemini-2.5-flash` | 250 req/day |
| `gemini-2.0-flash-lite` | fallback |
| `gemini-2.0-flash` | last resort |

---

## 🌐 Deploying to Streamlit Cloud

1. Push your code to a **public or private** GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch, and set `main.py` as the entry file
4. Under **Advanced settings → Secrets**, paste your `secrets.toml` contents
5. Click **Deploy**

---

## 🌍 Supported Languages

English · Hindi · Spanish · French · German · Portuguese · Arabic · Japanese · Chinese (Simplified) · Korean · Italian · Russian · Bengali · Gujarati · Marathi · Tamil · Telugu · Kannada · Punjabi · Dutch · Polish · Turkish · Vietnamese · Thai

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Google Gemini (via `google-generativeai`) |
| Email | Python `smtplib` + MIME |
| Styling | Custom CSS (Bebas Neue · DM Sans · JetBrains Mono) |

---

## 📋 Usage

1. **Paste** the email you received into the text area
2. **Select** your desired tone (Professional, Friendly, etc.)
3. **Choose** the language for your reply
4. *(Optional)* Enter a recipient email and any extra instructions
5. Click **⚡ GENERATE REPLY**
6. Review and edit the generated reply
7. Click **SEND EMAIL** to send, or **COPY TO CLIPBOARD** to use elsewhere

---

## ⚠️ Troubleshooting

**Generation failed / quota error**
> Wait a few minutes and retry. The app will automatically try the next available Gemini model. Check your quota at [aistudio.google.com](https://aistudio.google.com/).

**SMTP / sending failed**
> Ensure you're using a Gmail App Password, not your account password. Verify `SENDER_EMAIL`, `EMAIL_PASSWORD`, `SMTP_SERVER`, and `SMTP_PORT` in your secrets.

**Secrets not found (local)**
> Make sure `.streamlit/secrets.toml` exists at the project root and is correctly formatted TOML.

---

## 📄 License

All Rights Reserved © 2026 **Ravi Panchal**

---

<div align="center">
Made with ❤️ by <strong>Ravi Panchal</strong>
</div>