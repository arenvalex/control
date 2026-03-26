import random
import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler

TOKEN = "8675707540:AAFL_9t3xnAktDPZQSs-9YJeaPuqNqu_N5Y"
CHAT_ID = -1002241478647
ADMIN_ID = 8467771210

tz = pytz.timezone("Europe/Istanbul")

# -------- GİZLİ KOMUTLAR --------

async def yaz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        await update.message.delete()
    except:
        pass

    mesaj = " ".join(context.args)

    await context.bot.send_message(chat_id=CHAT_ID, text=mesaj)


async def troll(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        await update.message.delete()
    except:
        pass

    mesaj = random.choice(random_laf)

    await context.bot.send_message(chat_id=CHAT_ID, text=mesaj)


# -------- ALARMLAR --------

async def alarm1(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Her şey yolunda mı?")

async def alarm3(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Genel sahalardaki kasa uygunluğunu öğrenebilir miyiz?")

async def alarm4(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Mesai sırasında eğer 2 kişiyseniz 2 saatte bir yerlerinizi değiştiriniz.")

async def alarm5(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Sahalardaki bekleyen çekimleri kontrol edelim, uzun süre bekleyen varsa bilgi geçelim."
    )


# -------- GECECİ --------

gececi_mizah = [
"ALOOOOO gececi... panelde bekleyen çek varsa ben mi bakayım?",
"Gece uzun… ama panel daha uzun 😄"
]

async def gececi_troll(context):
    await context.bot.send_message(chat_id=CHAT_ID,text=random.choice(gececi_mizah))


# -------- EKİP --------

ekip_mizah = [
"ALOOOO ekip… herkes yaşıyor mu?",
"Şu anki ruh halim: %10 kahve, %20 panik, %70 'neyse ya hallederiz'",
"Panel sakin ama ben size güvenmiyorum kontrol edin 😄",
]

async def ekip_troll(context):
    await context.bot.send_message(chat_id=CHAT_ID,text=random.choice(ekip_mizah))

# -------- ÖZEL --------

async def gece_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Gececi arkadaşlara Allah kolaylık versin.")

async def sabah_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Sabah kuşlarım uyanmış mı yoksa hala offline mıyız 😄")

async def nobet_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Nöbetteyim!!")

async def oguz_mesaji(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="oguz uyan oguz sen uyursan herkes ölür :d")

async def gece_hatirlatma(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="ALOOOOOOOOOOOO bekleyen çekimleri 00:00'a göre ayarlat unutma!")


# -------- BOT --------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("yaz", yaz))
    app.add_handler(CommandHandler("troll", troll))

    job = app.job_queue

    job.run_daily(gece_mesaji,time(hour=0,minute=2,tzinfo=tz))
    job.run_daily(sabah_mesaji,time(hour=9,minute=0,tzinfo=tz))
    job.run_daily(gece_hatirlatma,time(hour=23,minute=50,tzinfo=tz))
    job.run_daily(nobet_mesaji,time(hour=5,minute=0,tzinfo=tz))
    job.run_daily(oguz_mesaji,time(hour=5,minute=12,tzinfo=tz))

    # GECECİ → 3 SAATTE 1
    for h in range(0,8,3):
        job.run_daily(gececi_troll,time(hour=h,minute=20,tzinfo=tz))

    # EKİP → 4 SAATTE 1
    for h in range(9,23,4):
        job.run_daily(ekip_troll,time(hour=h,minute=40,tzinfo=tz))

    # RANDOM → AYNI
    for h in [11,15,19]:
        job.run_daily(bot_random,time(hour=h,minute=10,tzinfo=tz))

    # KRİTİKLER (AYNI)
    for h in range(24):
        job.run_daily(alarm1,time(hour=h,minute=0,tzinfo=tz))

    for h in range(0,24,2):
        job.run_daily(alarm3,time(hour=h,minute=10,tzinfo=tz))

    for h in range(0,24,2):
        job.run_daily(alarm4,time(hour=h,minute=5,tzinfo=tz))

    for h in range(24):
        job.run_daily(alarm5,time(hour=h,minute=15,tzinfo=tz))

    print("Bot aktif")

    app.run_polling()


if __name__ == "__main__":
    main()
