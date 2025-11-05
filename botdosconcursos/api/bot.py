import os
from flask import Flask, request
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8231368795:AAGK95Q-X1XkVO0hsKJJZtjSiBjTzot18iE")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://botdosconcursos.vercel.app/api/bot")

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Acesso Premium", callback_data='premium')],
        [InlineKeyboardButton("🧾 Conteúdo Grátis", callback_data='gratis')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Eu sou o *BotDosConcursos*!\n\n"
        "Ofereço conteúdos para quem quer passar em concursos públicos 💪\n"
        "Escolha uma opção abaixo:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def gratis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📘 Conteúdo gratuito disponível:\n\n"
        "- Dicas de estudo\n"
        "- Cronograma semanal\n"
        "- Artigos motivacionais\n\n"
        "Para ter acesso a *materiais premium (PDFs, simulados, videoaulas)*, use o comando /premium.",
        parse_mode='Markdown'
    )

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 *Acesso Premium do BotDosConcursos*\n\n"
        "Tenha acesso a:\n"
        "✅ PDFs exclusivos\n"
        "✅ Videoaulas e simulados\n"
        "✅ Questões e provas anteriores\n"
        "✅ Atualizações semanais\n\n"
        "Assine por apenas *R$9,90/mês* 👇\n"
        "[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)"
    )
    await update.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)

async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "💎 *Acesso Premium do BotDosConcursos*\n\n"
        "Acesse seu plano:\n[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)",
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("premium", premium))
application.add_handler(CallbackQueryHandler(gratis, pattern='^gratis$'))
application.add_handler(CallbackQueryHandler(premium_callback, pattern='^premium$'))

@app.route("/api/bot", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "🤖 BotDosConcursos está online (modo Webhook)."

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    res = requests.get(url)
    return res.text
