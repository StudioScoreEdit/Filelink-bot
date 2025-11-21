# Filelink-bot

A simple Telegram File → Direct Link bot (Python + Pyrogram).  
Send a file to the bot, it downloads once and serves a fast direct HTTP link.

## Files in repo
- bot.py         -> Telegram bot logic
- server.py      -> HTTP server with range support (stream & resume)
- requirements.txt
- Procfile       -> for Railway
- .env.example

## How to deploy (Railway)
1. Add this repo to GitHub.
2. Create a Railway project → Deploy from GitHub.
3. Add Railway variables (API_ID, API_HASH, BOT_TOKEN, APP_URL, PORT).
4. Update `.env` APP_URL after Railway gives your URL.
