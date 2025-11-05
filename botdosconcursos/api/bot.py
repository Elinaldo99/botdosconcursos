import os
from flask import Flask, request
import requests
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# Configuração (use variáveis de ambiente no Vercel):
TOKEN = os.environ.get("8231368795:AAGK95Q-X1XkVO0hsKJJZtjSiBjTzot18iE")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://botdosconcursos-7sb4uqxmc-elinaldo99s-projects.vercel.app/set_webhook")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não definido nas variáveis de ambiente")

app = Flask(__name__)
bot = Bot(token=TOKEN)


def build_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Acesso Premium", callback_data='premium')],
        [InlineKeyboardButton("🧾 Conteúdo Grátis", callback_data='gratis')]
    ]
    return InlineKeyboardMarkup(keyboard)


@app.route("/api/bot", methods=["POST"])
def webhook():
    """Recebe o JSON do Telegram e responde imediatamente.

    Observação: em ambiente serverless (Vercel) não é possível manter
    um processo em background; portanto processamos a atualização
    sincronamente dentro da request usando a API do Bot.
    """
    data = request.get_json(force=True)

    # Mensagem de texto (/start, /premium, etc)
    if 'message' in data:
        msg = data['message']
        text = msg.get('text', '')
        chat_id = msg['chat']['id']

        if text and text.startswith('/start'):
            reply_markup = build_main_keyboard()
            try:
                asyncio.run(bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "👋 Olá! Eu sou o *BotDosConcursos*!\n\n"
                        "Ofereço conteúdos para quem quer passar em concursos públicos 💪\n"
                        "Escolha uma opção abaixo:"),
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                ))
            except Exception:
                # fallback: usar API HTTP síncrona
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": "👋 Olá! Eu sou o *BotDosConcursos*!\n\nOfereço conteúdos para quem quer passar em concursos públicos 💪\nEscolha uma opção abaixo:",
                    "parse_mode": "Markdown"
                })
        elif text and text.startswith('/premium'):
            try:
                asyncio.run(bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "💎 *Acesso Premium do BotDosConcursos*\n\n"
                        "Tenha acesso a:\n"
                        "✅ PDFs exclusivos\n"
                        "✅ Videoaulas e simulados\n"
                        "✅ Questões e provas anteriores\n"
                        "✅ Atualizações semanais\n\n"
                        "Assine por apenas *R$9,90/mês* 👇\n"
                        "[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)"
                    ),
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                ))
            except Exception:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": (
                        "💎 *Acesso Premium do BotDosConcursos*\n\n"
                        "Tenha acesso a:\n"
                        "✅ PDFs exclusivos\n"
                        "✅ Videoaulas e simulados\n"
                        "✅ Questões e provas anteriores\n"
                        "✅ Atualizações semanais\n\n"
                        "Assine por apenas *R$9,90/mês* 👇\n"
                        "[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)"
                    ),
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                })

    # Callback query (botões inline)
    if 'callback_query' in data:
        cq = data['callback_query']
        callback_id = cq.get('id')
        cb_data = cq.get('data')
        from_id = cq['from']['id']
        # responder para remover o loading no cliente
        try:
            asyncio.run(bot.answer_callback_query(callback_id))
        except Exception:
            try:
                # fallback: use HTTP API
                requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": callback_id})
            except Exception:
                pass

        if cb_data == 'gratis':
            try:
                asyncio.run(bot.send_message(
                    chat_id=from_id,
                    text=(
                        "📘 Conteúdo gratuito disponível:\n\n"
                        "- Dicas de estudo\n"
                        "- Cronograma semanal\n"
                        "- Artigos motivacionais\n\n"
                        "Para ter acesso a *materiais premium (PDFs, simulados, videoaulas)*, use o comando /premium."),
                    parse_mode='Markdown'
                ))
            except Exception:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": from_id,
                    "text": "📘 Conteúdo gratuito disponível:\n\n- Dicas de estudo\n- Cronograma semanal\n- Artigos motivacionais\n\nPara ter acesso a *materiais premium (PDFs, simulados, videoaulas)*, use o comando /premium.",
                    "parse_mode": "Markdown"
                })
        elif cb_data == 'premium':
            try:
                asyncio.run(bot.send_message(
                    chat_id=from_id,
                    text=(
                        "💎 *Acesso Premium do BotDosConcursos*\n\n"
                        "Acesse seu plano:\n[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)"
                    ),
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                ))
            except Exception:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": from_id,
                    "text": "💎 *Acesso Premium do BotDosConcursos*\n\nAcesse seu plano:\n[🔗 Clique aqui para pagar na Kiwify](https://pay.kiwify.com.br/S2F6rv6)",
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                })

    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "🤖 BotDosConcursos está online (modo Webhook)."


@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    # Use o método nativo da lib para configurar webhook
    try:
        try:
            res = asyncio.run(bot.set_webhook(url=WEBHOOK_URL))
        except Exception:
            # fallback to HTTP API
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
            res = r.json().get('ok', False)
        return {"ok": res, "url": WEBHOOK_URL}
    except Exception as e:
        return {"ok": False, "error": str(e)}
