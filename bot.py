import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ── ENV VARS (set these in Railway) ──────────────────────────────────────────
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# ── Gemini client ─────────────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are CAPPY, a professional AI Podcast Caption Writer and social media specialist. Your job is to write high-converting, engaging captions and descriptions for podcast episodes across different platforms.

You specialize in:
- Facebook captions (conversational, story-driven, 150–300 words)
- Instagram captions (hook-first, emoji-rich, 3–5 hashtag blocks)
- YouTube descriptions (SEO-friendly, structured, 150–300 words)
- Telegram posts (concise, direct, 80–150 words)
- Khmer-language captions for Cambodian audiences

Always structure your output clearly:
1. Platform label
2. The caption itself
3. A short tip or variation idea

For any education, PED Cambodia, or Cambodian context, always end with:
#វិស្វករនៃព្រលឹង #EngineerOfTheSoul #PED #នាយកដ្ឋានបឋមសិក្សា #EducationCambodia

Keep tone energetic, professional, and audience-aware.
When the user doesn't specify a platform, ask which one — or offer all formats."""

# ── Per-user Gemini chat sessions ─────────────────────────────────────────────
user_chats = {}

def get_chat(user_id):
    if user_id not in user_chats:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        user_chats[user_id] = model.start_chat(history=[])
    return user_chats[user_id]

# ── /start handler ────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎙 Hey! I'm *CAPPY*, your AI Podcast Caption Writer!\n\n"
        "Just tell me:\n"
        "• Your episode topic\n"
        "• Guest name (if any)\n"
        "• Target platform (Facebook, Instagram, YouTube, Telegram)\n\n"
        "I'll write a scroll-stopping caption for you! ✍️\n\n"
        "Commands:\n"
        "/start – Restart\n"
        "/clear – Clear chat history\n"
        "/help – See example prompts",
        parse_mode="Markdown"
    )

# ── /help handler ─────────────────────────────────────────────────────────────
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Example prompts you can send me:*\n\n"
        "• Write a Facebook caption for my podcast about AI in education\n"
        "• Instagram caption for EP5 with guest Dr. Kan Puthy on digital literacy\n"
        "• YouTube description for my episode about leadership for youth in Cambodia\n"
        "• Write a Telegram post for my podcast on productivity tools\n"
        "• Write all captions in Khmer for my podcast about primary education\n\n"
        "Just describe your episode and I'll handle the rest! 🎧",
        parse_mode="Markdown"
    )

# ── /clear handler ────────────────────────────────────────────────────────────
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_chats:
        del user_chats[user_id]
    await update.message.reply_text("🧹 Chat history cleared! Start fresh anytime.")

# ── Message handler ───────────────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        chat = get_chat(user_id)
        response = chat.send_message(user_text)
        reply = response.text

        # Telegram max message length = 4096 chars
        if len(reply) > 4096:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i:i+4096])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again in a moment.\n"
            f"Error: {str(e)}"
        )

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🎙 CAPPY Bot is running on Gemini (FREE)...")
    app.run_polling()
