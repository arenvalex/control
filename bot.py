import os
import random
import asyncio
import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8675707540:AAHgenEKFtA-HiqRZhTYfkWdbdMsnl5g89A")
CHAT_ID = int(os.getenv("1002241478647"))

tz = pytz.timezone("Europe/Istanbul")

# -------- OTOMATİK CEVAPLAR --------

kolay_cevaplar = [
"Hoş geldin, kolay gelsin 🙌",
"Sana da kolay gelsin 💪",
"Hoş geldin iyi mesailer",
"Kolay gelsin, iyi çalışmalar",
"Hoş geldin, güzel bir mesai olsun"
]

async def mesaj_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "selam" in text:
        await update.message.reply_text("Selamlar hoş geldin")

    elif "kolay gelsin" in text:
        await update.message.reply_text(random.choice(kolay_cevaplar))

# -------- ALARMLAR --------

async def alarm1(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Her şey yolunda mı?"
    )

async def alarm2(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Gönderilmeyi bekleyen çekim kaç tane? Bekleme sebebiyle yazınız."
    )

async def alarm3(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Sahalara test yatırım talebi oluşturunuz."
    )

async def alarm4(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="""Mesai sırasında eğer 2 kişiyseniz
2 saatte bir yerlerinizi değiştiriniz."""
    )

async def alarm5(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="lütfen sahalardaki bekleyen çekimleri kontrol ediniz. uzun süre bekleyen varsa sahaya iletiniz."
    )

# -------- BOT --------

async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mesaj_kontrol))

    job = app.job_queue

    # her saat başı
    job.run_repeating(alarm1, interval=3600, first=5)

    # her saat 30
    job.run_repeating(alarm2, interval=3600, first=1800)

    # 2 saatte bir 10 geçe
    for h in range(0, 24, 2):
        job.run_daily(alarm3, time(hour=h, minute=10, tzinfo=tz))

    # 2 saatte bir 05 geçe
    for h in range(0, 24, 2):
        job.run_daily(alarm4, time(hour=h, minute=5, tzinfo=tz))

    # 15 dakikada bir
    job.run_repeating(alarm5, interval=900, first=10)

    print("Bot aktif")

    await app.run_polling()

asyncio.run(main())
