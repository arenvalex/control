import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

TOKEN = "8675707540:AAFL_9t3xnAktDPZQSs-9YJeaPuqNqu_N5Y"
CHAT_ID = -1002241478647
ADMIN_ID = 8467771210

tz = pytz.timezone("Europe/Istanbul")

# -------- MESAJ SİLME --------

async def mesaj_sil(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(
            chat_id=job.data["chat_id"],
            message_id=job.data["message_id"]
        )
    except:
        pass


# -------- GÖNDER + 10 DK SONRA SİL --------

async def gonder_ve_sil(context, text):
    msg = await context.bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )

    # 10 dakika sonra sil
    context.job_queue.run_once(
        mesaj_sil,
        when=600,
        data={
            "chat_id": CHAT_ID,
            "message_id": msg.message_id
        }
    )


# -------- GİZLİ KOMUT --------

async def yaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        await update.message.delete()
    except:
        pass

    mesaj = " ".join(context.args)

    msg = await context.bot.send_message(chat_id=CHAT_ID, text=mesaj)

    # 10 dk sonra sil
    context.job_queue.run_once(
        mesaj_sil,
        when=600,
        data={
            "chat_id": CHAT_ID,
            "message_id": msg.message_id
        }
    )


# -------- MESAJLAR --------

async def alarm1(context):
    await gonder_ve_sil(context, "Her şey yolunda mı? Lütfen Mesajı alıntılayarak sorun var ise bildiriniz!")

async def alarm3(context):
    await gonder_ve_sil(context, "Genel sahalardaki kasa uygunluğunu öğrenebilir miyiz? Lütfen Mesajı alıntılayarak uygunluk listesini iletiniz!")

async def alarm4(context):
    await gonder_ve_sil(context, "Mesai sırasında eğer 2 kişiyseniz 2 saatte bir yerlerinizi değiştiriniz. Değişim sonrası görev yerlerinizi alıntı yaparak cevap veriniz!")

async def alarm5(context):
    await gonder_ve_sil(context, "Sahalardaki bekleyen çekimleri kontrol edelim, uzun süre bekleyen varsa bilgi geçelim. VİP ve PREVİP oyunculara öncelik verelim eğer çekim gitmeyecekse manuel gönderelim!")

async def gece_mesaji(context):
    await gonder_ve_sil(context, "Gececi arkadaşlara Allah kolaylık versin.")

async def gece_hatirlatma(context):
    await gonder_ve_sil(context, "ALOOOOOOOOOOOO bekleyen çekimleri 00:00'a göre ayarlat unutma!")


# -------- BOT --------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("yaz", yaz))

    job = app.job_queue

    # GECE MESAJLARI
    job.run_daily(gece_mesaji, time(hour=0, minute=2, tzinfo=tz))
    job.run_daily(gece_hatirlatma, time(hour=23, minute=50, tzinfo=tz))

    # SAAT BAŞI → KASA
    job.run_repeating(alarm3, interval=3600, first=0)

    # SAAT BAŞI +10 DK → GENEL DURUM
    job.run_repeating(alarm1, interval=3600, first=600)

    # 35 DK → ÇEKİM
    job.run_repeating(alarm5, interval=2100, first=0)

    # 2 SAAT → YER DEĞİŞTİRME
    job.run_repeating(alarm4, interval=7200, first=0)

    print("Bot aktif")
    app.run_polling()


if __name__ == "__main__":
    main()
