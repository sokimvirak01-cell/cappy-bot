# 🎙 CAPPY — AI Podcast Caption Writer Bot (FREE with Gemini)

A Telegram bot powered by Google Gemini AI (FREE tier) that writes professional captions for podcast episodes.

---

## 🆓 Gemini Free Tier Limits
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute
- Completely FREE — no credit card needed!

---

## 🚀 Deploy on Railway

### Step 1 — Get your tokens

**Telegram Token:**
1. Open Telegram → search @BotFather
2. Send /newbot
3. Follow steps → copy your token

**Gemini API Key (FREE):**
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key — no credit card needed!

### Step 2 — Upload to GitHub
1. Create account at https://github.com
2. Create new repo (e.g. cappy-bot)
3. Upload: bot.py, requirements.txt, Procfile

### Step 3 — Deploy on Railway
1. Go to https://railway.app → sign in with GitHub
2. Click New Project → Deploy from GitHub repo
3. Select your cappy-bot repo
4. Go to Variables tab and add:
   - TELEGRAM_TOKEN = your token from BotFather
   - GEMINI_API_KEY = your key from Google AI Studio
5. Railway auto-deploys → your bot goes live! ✅

---

## 💬 Bot Commands

| Command | Action |
|---------|--------|
| /start  | Welcome message |
| /help   | Example prompts |
| /clear  | Clear conversation history |

---

## 📝 Example Messages

- "Write a Facebook caption for my podcast about AI in education"
- "Instagram caption for EP5 with guest Dr. Kan Puthy on digital literacy"
- "YouTube description for my episode about youth leadership in Cambodia"
- "Write all captions in Khmer for my podcast about primary education"
