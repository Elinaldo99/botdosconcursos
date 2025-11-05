# BotDosConcursos

Este diretório contém o código do bot Telegram e instruções para deploy no Vercel.

## O que foi feito
- O bot foi adaptado para rodar em ambiente serverless (Vercel) processando updates síncronamente na rota `/api/bot`.
- Adicionado `vercel.json` para configurar o builder Python e rotas.

## Variáveis de ambiente (defina no Vercel ou localmente)
- `TELEGRAM_BOT_TOKEN` (obrigatório): token do seu bot Telegram (ex: `123456:ABC-DEF...`).
- `WEBHOOK_URL` (opcional): URL pública que o Telegram usará para enviar updates (ex: `https://<seu-deploy>.vercel.app/api/bot`).

## Testando localmente (recomendado antes do deploy)
1. Criar virtualenv e instalar dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Exportar variável do token (use seu token real ou temporário para testes):

```bash
export TELEGRAM_BOT_TOKEN="seu_token_aqui"
```

3. Rodar Flask localmente (apenas para desenvolvimento):

```bash
cd api
export FLASK_APP=bot.py
flask run --port 5000
```

4. Testar enviando um update de exemplo:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"update_id":1,"message":{"message_id":1,"from":{"id":123},"chat":{"id":123,"type":"private"},"text":"/start"}}' \
  http://127.0.0.1:5000/api/bot
```

Você deverá receber resposta `ok` (HTTP 200) e o bot tentará enviar uma mensagem para o chat (use um token real para ver mensagens no Telegram).

## Deploy no Vercel
1. Commit e push para o repositório conectado ao Vercel.
2. No painel do Vercel, defina as variáveis de ambiente do projeto:
   - `TELEGRAM_BOT_TOKEN` = seu token do bot
   - `WEBHOOK_URL` = `https://<seu-deployment>.vercel.app/api/bot` (recomendado)
3. Após o deploy, acesse `https://<seu-deployment>.vercel.app/set_webhook` para registrar o webhook no Telegram. Deve retornar `{"ok": true, "url": "..."}`.

## Observações
- Em serverless não há processos em background. Por isso o bot foi implementado para processar cada update na própria requisição.
- Para funcionalidades que exigem jobs em background (tarefas recorrentes), considere hospedar em um serviço com processo persistente.
