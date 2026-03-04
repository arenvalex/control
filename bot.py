import random
import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8675707540:AAHgenEKFtA-HiqRZhTYfkWdbdMsnl5g89A"
CHAT_ID = -1002241478647

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
    
async def sabah_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="""☀️ Günaydın ekip

Yeni bir gün başladı.
Herkese hatasız ve sorunsuz mesailer dileriz.
Kolay gelsin 💪""")

async def ogle_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="""☕ Saat 12 oldu

Kahveleri alalım biraz enerji toplayalım.
Herkese hatasız mesailer dileriz.""")

async def aksam_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="""🔄 Yeni ekip hoş geldiniz

Devralan ekibe iyi mesailer.
Sahalar ve çekimler kontrol edilerek devam edelim.""")

async def gece_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="""🌙 Gece mesaisi başlamıştır

Gece ekibine sakin ve sorunsuz bir mesai dileriz.
Kolay gelsin.""")
    
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mesaj_kontrol))

    job = app.job_queue

    # ---- GÜNLÜK MESAJLAR ----

    job.run_daily(sabah_mesaji, time(hour=8, minute=0, tzinfo=tz))
    job.run_daily(ogle_mesaji, time(hour=12, minute=0, tzinfo=tz))
    job.run_daily(aksam_mesaji, time(hour=16, minute=0, tzinfo=tz))
    job.run_daily(gece_mesaji, time(hour=0, minute=2, tzinfo=tz))

    # -------- HER SAAT BAŞI --------
    for h in range(24):
        job.run_daily(alarm1, time(hour=h, minute=0, tzinfo=tz))

    # -------- HER SAAT 30 --------
    for h in range(24):
        job.run_daily(alarm2, time(hour=h, minute=30, tzinfo=tz))

    # -------- 2 SAATTE BİR 10 GEÇE --------
    for h in range(0, 24, 2):
        job.run_daily(alarm3, time(hour=h, minute=10, tzinfo=tz))

    # -------- 2 SAATTE BİR 05 GEÇE --------
    for h in range(0, 24, 2):
        job.run_daily(alarm4, time(hour=h, minute=5, tzinfo=tz))

    # -------- HER SAAT 15 GEÇE --------
    for h in range(24):
        job.run_daily(alarm5, time(hour=h, minute=15, tzinfo=tz))

    print("Bot aktif")

    app.run_polling()

if __name__ == "__main__":
    main()
