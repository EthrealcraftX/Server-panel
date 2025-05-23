from pyrogram import Client, filters
from pyrogram.types import Message
from collections import defaultdict
import json
import os

# API va TOKEN
API_ID = 13064636
API_HASH = "42eb9677330d23211ff7397d0a446333"
BOT_TOKEN = "7223441901:AAFFL4-sqarL-JptCoQhTqiqgw8eVRW99Ik"

DATA_FILE = "user_data.json"

# Yordamchi: ma'lumotlarni saqlash va yuklash
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return defaultdict(int, json.load(f))
    return defaultdict(int)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_counter = load_data()

app = Client("user_adder_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.new_chat_members)
async def track_new_members(client: Client, message: Message):
    adder = message.from_user
    if adder:
        for new_member in message.new_chat_members:
            if new_member.id != adder.id:
                user_counter[str(adder.id)] += 1
                save_data(user_counter)

@app.on_message(filters.command("stat") & filters.group)
async def show_stats(client: Client, message: Message):
    if not user_counter:
        await message.reply_text("Hali hech kim hech kimni qo‘shmagan.")
        return

    sorted_users = sorted(user_counter.items(), key=lambda x: x[1], reverse=True)
    msg = "**Foydalanuvchilar qo‘shganlar statistikasi:**\n\n"
    for i, (user_id, count) in enumerate(sorted_users, start=1):
        try:
            user = await client.get_users(int(user_id))
            msg += f"{i}. {user.mention} — {count} ta\n"
        except:
            msg += f"{i}. [Foydalanuvchi](tg://user?id={user_id}) — {count} ta\n"

    await message.reply_text(msg)

@app.on_message(filters.command("reset") & filters.group)
async def reset_stats(client: Client, message: Message):
    if message.from_user and message.from_user.id == message.chat.id:
        await message.reply_text("Bu komanda faqat guruh adminlari uchun.")
        return

    user_counter.clear()
    save_data(user_counter)
    await message.reply_text("Statistika tozalandi.")

print("✅ Bot ishga tushdi")
app.run()
