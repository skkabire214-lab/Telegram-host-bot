import logging
import subprocess
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Apnar numeric Telegram User ID bosiye din (jemon: 123456789)
ADMIN_ID = 6477403171  

running_processes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return
    await update.message.reply_text("Host Bot Active! Send me any `.py` script to run it.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    document = update.message.document
    file_name = document.file_name

    if not file_name.endswith('.py'):
        await update.message.reply_text("Please send a valid Python (.py) file.")
        return

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_name)

    await update.message.reply_text(f"File `{file_name}` received. Starting script...")

    try:
        process = subprocess.Popen(["python", file_name])
        running_processes[file_name] = process
        await update.message.reply_text(f"✅ `{file_name}` is now RUNNING! PID: {process.pid}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error starting script: {str(e)}")

async def stop_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /stop filename.py")
        return

    file_name = context.args[0]
    if file_name in running_processes:
        process = running_processes[file_name]
        process.kill()
        del running_processes[file_name]
        await update.message.reply_text(f"🛑 Stopped `{file_name}` successfully.")
    else:
        await update.message.reply_text("Script not found or not running.")

if __name__ == "__main__":
    # BotFather theke pawa Token bosiye din
    BOT_TOKEN = "7958284176:AAFdWIdoKDHVOOSzVV2nJcXkPLHmhVmwhXs"  

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop_script))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Host Bot is running...")
    app.run_polling()
