import os, asyncio, threading
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

TOKEN = "".join(os.environ.get("TG_TOKEN", "").split())
MY_ID = int("".join(os.environ.get("TG_USER_ID", "0").split()))


_app = None
_loop = None
_waiting = False

def start_bot(send_to_neo_alpha):
    if not TOKEN or not MY_ID:
        print("[Telegram] token or user id missing, bot not started")
        return

    async def on_msg(update: Update, context):
        global _waiting
        if update.effective_user.id != MY_ID:
            return

        t = update.message.text.lower()
        if any(w in t for w in ["screenshot", "screen shot", "snip", "screen capture", "print screen", "my screen"]):
            try:
                from PIL import ImageGrab
                ImageGrab.grab().save("shot.png")
                with open("shot.png", "rb") as f:
                    await update.message.reply_photo(f, write_timeout=60, read_timeout=60, connect_timeout=60)
                print("[Telegram] screenshot sent")
            except Exception as e:
                print("[Telegram] screenshot error:", e)
                await update.message.reply_text(f"screenshot failed: {e}")
            return
        
        _waiting = True
        send_to_neo_alpha(update.message.text)

    async def on_photo(update: Update, context):
        if update.effective_user.id != MY_ID:
            return
        try:
            from google import genai
            from google.genai import types
            tg_file = await update.message.photo[-1].get_file()
            data = bytes(await tg_file.download_as_bytearray())
            question = update.message.caption or "Explain what's in this image, briefly."
            client = genai.Client(api_key=get_key())
            resp = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-3.8-flash",
                contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg"), question],
            )
            await update.message.reply_text(resp.text or "couldn't read that one")
        except Exception as e:
            print("[Telegram] photo error:", e)
            await update.message.reply_text(f"photo failed: {e}")

    def run():
        global _app, _loop
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
        _app = Application.builder().token(TOKEN).build()
        _app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
        _app.add_handler(MessageHandler(filters.PHOTO, on_photo))
        _app.run_polling(stop_signals=None)

    threading.Thread(target=run, daemon=True).start()

def reply(text):
    global _waiting
    if not _waiting or not _app or not _loop or not text:
        return
    _waiting = False
    asyncio.run_coroutine_threadsafe(
        _app.bot.send_message(chat_id=MY_ID, text=text), _loop)