import random
import pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8675707540:AAHgenEKFtA-HiqRZhTYfkWdbdMsnl5g89A"
CHAT_ID = -1002241478647

tz = pytz.timezone("Europe/Istanbul")

# -------- SOHBET --------

selam_cevaplar = [
"Hoş geldin baba kolay gele",
"Cehenneme hoş geldin 😄",
"Selam kral hoş geldin",
"Hoş geldin reis"
]

kolay_cevaplar = [
"Sana da kolay gelsin 💪",
"Eyvallah sana da kolay gelsin",
"Kolay gelsin ekip",
"Kolay gelsin kral"
]

async def mesaj_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "selam" in text:
        await update.message.reply_text(random.choice(selam_cevaplar))

    elif "kolay gelsin" in text:
        await update.message.reply_text(random.choice(kolay_cevaplar))


# -------- ALARMLAR --------

async def alarm1(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Her şey yolunda mı?")

async def alarm3(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Sahalara test yatırım talebi oluşturunuz.")

async def alarm4(context):
    await context.bot.send_message(chat_id=CHAT_ID,text="Mesai sırasında eğer 2 kişiyseniz 2 saatte bir yerlerinizi değiştiriniz.")

async def alarm5(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Lütfen sahalardaki bekleyen çekimleri kontrol ediniz. Uzun süre bekleyen varsa sahaya iletiniz."
        
async def arda_mesaji(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Bu Lara çok olmaya başladı sürekli bana Arda'nın dedikodusunu yapıyor"
            
    )


# -------- GECECİ MESAJLARI --------

gececi_mizah = [
"ALOOOOO gececi... panelde bekleyen çek varsa ben mi bakayım?",
"Uyuma lan… sahalarda biri bekliyorsa ayıp olur 😄",
"Bir bakın şu sahalara, bot olarak ben utanıyorum artık",
"Panel sessiz… siz de mi sessiz? şüphelendim şimdi 👀",
"Burada kimse yoksa ben kapatıyorum ışıkları 😄",
"Gececi kardeşim çay koyduysan bana da söyle",
"Gece uzun… ama panel daha uzun 😄"
]

async def gececi_troll(context):
    await context.bot.send_message(chat_id=CHAT_ID,text=random.choice(gececi_mizah))


# -------- EKİP MESAJLARI --------

ekip_mizah = [
"ALOOOO ekip… herkes yaşıyor mu?",
"Bu sessizlik hiç hayra alamet değil",
"Panel sakin ama ben size güvenmiyorum kontrol edin 😄",
"Bir sahalara bakın da içimiz rahat etsin",
"Bot olarak görevimi yapıyorum… siz de yapın 😄",
"ALOOOOOOOOOOOO ekip hayattayız dimi?",
"Ben botum ama ben bile panik yaptım 😄"
]

async def ekip_troll(context):
    await context.bot.send_message(chat_id=CHAT_ID,text=random.choice(ekip_mizah))


# -------- RANDOM BOT --------

random_laf = [
"Ben burada çalışıyorum siz napıyorsunuz 😄",
"Ekip sahalar nasıl?",
"Panel sakin ama ben tetikteyim 👀",
"Her şey yolundaysa devam 👍"
]

async def bot_random(context):
    await context.bot.send_message(chat_id=CHAT_ID,text=random.choice(random_laf))


# -------- ÖZEL MESAJLAR --------

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

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mesaj_kontrol))

    job = app.job_queue

    job.run_daily(gece_mesaji,time(hour=0,minute=2,tzinfo=tz))
    job.run_daily(sabah_mesaji,time(hour=9,minute=0,tzinfo=tz))
    job.run_daily(gece_hatirlatma,time(hour=23,minute=50,tzinfo=tz))
    job.run_daily(nobet_mesaji,time(hour=5,minute=0,tzinfo=tz))
    job.run_daily(oguz_mesaji,time(hour=5,minute=12,tzinfo=tz))
    job.run_daily(arda_mesaji, time(hour=1, minute=30, tzinfo=tz))
    
    # GECECİ DÜRTME
    for h in range(0,8):
        job.run_daily(gececi_troll,time(hour=h,minute=20,tzinfo=tz))

    # EKİP DÜRTME
    for h in range(9,23):
        job.run_daily(ekip_troll,time(hour=h,minute=40,tzinfo=tz))

    # RANDOM BOT
    for h in [11,15,19]:
        job.run_daily(bot_random,time(hour=h,minute=10,tzinfo=tz))

    # HER SAAT
    for h in range(24):
        job.run_daily(alarm1,time(hour=h,minute=0,tzinfo=tz))

    # 2 SAATTE BİR
    for h in range(0,24,2):
        job.run_daily(alarm3,time(hour=h,minute=10,tzinfo=tz))

    for h in range(0,24,2):
        job.run_daily(alarm4,time(hour=h,minute=5,tzinfo=tz))

    # HER SAAT 15
    for h in range(24):
        job.run_daily(alarm5,time(hour=h,minute=15,tzinfo=tz))

    print("Bot aktif")

    app.run_polling()

if __name__ == "__main__":
    main()
