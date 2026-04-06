import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

TOKEN = "8675707540:AAFL_9t3xnAktDPZQSs-9YJeaPuqNqu_N5Y"
CHAT_ID = -1002241478647
ADMIN_ID = 8467771210

tz = pytz.timezone("Europe/Istanbul")

# -------- GİZLİ KOMUT --------

async def yaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        await update.message.delete()
    except:
        pass

    mesaj = " ".join(context.args)
    await context.bot.send_message(chat_id=CHAT_ID, text=mesaj)


# -------- MESAJLAR --------

async def alarm1(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Her şey yolunda mı? Lütfen Mesajı alıntılayarak sorun var ise bildiriniz!"
    )

async def alarm3(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Genel sahalardaki kasa uygunluğunu öğrenebilir miyiz? Lütfen Mesajı alıntılayarak uygunluk listesini iletiniz!"
    )

async def alarm4(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Mesai sırasında eğer 2 kişiyseniz 2 saatte bir yerlerinizi değiştiriniz. Değişim sonrası görev yerlerinizi alıntı yaparak cevap veriniz!"
    )

async def alarm5(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Sahalardaki bekleyen çekimleri kontrol edelim, uzun süre bekleyen varsa bilgi geçelim. VİP ve PREVİP oyunculara öncelik verelim eğer çekim gitmeyecekse manuel gönderelim!"
    )

async def gece_mesaji(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Gececi arkadaşlara Allah kolaylık versin."
    )

async def gece_hatirlatma(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="ALOOOOOOOOOOOO bekleyen çekimleri 00:00'a göre ayarlat unutma!"
    )


# -------- BOT --------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("yaz", yaz))

    job = app.job_queue

    # GECE MESAJLARI
    job.run_daily(gece_mesaji, time(hour=0, minute=2, tzinfo=tz))
    job.run_daily(gece_hatirlatma, time(hour=23, minute=50, tzinfo=tz))

    # SAAT BAŞI → KASA (00:00, 01:00, ...)
    job.run_repeating(alarm3, interval=3600, first=0)

    # SAAT BAŞI +10 DK → GENEL DURUM (00:10, 01:10, ...)
    job.run_repeating(alarm1, interval=3600, first=600)

    # 35 DK → ÇEKİM
    job.run_repeating(alarm5, interval=2100, first=0)

    # 2 SAAT → YER DEĞİŞTİRME
    job.run_repeating(alarm4, interval=7200, first=0)

    print("Bot aktif")
    app.run_polling()


if __name__ == "__main__":
    main()
