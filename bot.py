from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
import os

BOT_TOKEN = 'https://t.me/+8nLv-fN8G800NWZk'

async def start(update: Update, context):
    await update.message.reply_text("أهلاً! أرسل لي رابط يوتيوب وسأقوم بتحميله لك.")

async def download(update: Update, context):
    url = update.message.text
    await update.message.reply_text("جاري تحميل الفيديو... يرجى الانتظار")
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': 'video.%(ext)s',
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        filename = 'video.mp4'
        if not os.path.exists(filename):
            for file in os.listdir('.'):
                if file.startswith('video'):
                    filename = file
                    break
        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"فشل التحميل: {str(e)}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
print("البوت يعمل...")
app.run_polling()