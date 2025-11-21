import os
import uuid
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL").rstrip("/")
PORT = int(os.getenv("PORT", 8080))
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

FILE_MAP = {}

async def start_server():
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=PORT)

@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def file_handler(client, m):
    await m.reply("Downloading…")

    if m.photo:
        name = f"{uuid.uuid4().hex}.jpg"
    else:
        name = m.document.file_name or f"file_{uuid.uuid4().hex}"

    file_id = uuid.uuid4().hex
    path = DOWNLOAD_DIR / f"{file_id}_{name}"

    await m.download(file_name=str(path))

    url = f"{APP_URL}/d/{file_id}/{name}"
    await m.reply(f"Your Direct Link:\n{url}")

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("Send me a file to get a direct chrome link.")

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    app.run()

if __name__ == "__main__":
    main()
