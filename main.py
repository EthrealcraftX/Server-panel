from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import uvicorn
from fastapi import FastAPI
import os

# === BOT SOZLAMALARI ===
API_ID = int(os.getenv("API_ID", "13064636"))
API_HASH = os.getenv("API_HASH", "42eb9677330d23211ff7397d0a446333")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7223441901:AAFFL4-sqarL-JptCoQhTqiqgw8eVRW99Ik")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID", "-1002645346805"))

app = Client("service_cleaner_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# === FAQAT SERVICE XABARLARNI DELETE QILISH ===
@app.on_message(filters.group & filters.service)
def delete_service_messages(client: Client, message: Message):
    if message.chat.id == ALLOWED_GROUP_ID:
        try:
            message.delete()
        except:
            pass  # jim turadi

# === FASTAPI WEB SERVER (port 8000 uchun) ===
web_app = FastAPI()

@web_app.get("/")
def root():
    return {"status": "Bot is running!"}

# === WEB SERVERNI ALOHIDA IPLICHADA ISHLATISH ===
def run_web():
    uvicorn.run(web_app, host="0.0.0.0", port=8000)

# === HAMMA NARSANI ISHLATISH ===
if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web)
    web_thread.start()
    app.run()