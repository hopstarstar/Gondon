
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ТВОЇ ДАНІ
TOKEN = '8107838667:AAGy84WVK1nLT35XS8QIb0MzrN0hoIgxfQw'
ADMIN_ID = 7005644725  # БЕЗ лапок, просто цифри

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вітаю! Надішліть номер замовлення, ми перевіримо його статус.")

# Коли користувач пише повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # Відповідаємо користувачу
    await update.message.reply_text("Зачекайте, йде перевірка...")

    # Надсилаємо повідомлення адмінам
    message_to_admin = f"Нове замовлення!

Від @{username} (ID: {user_id})
Повідомлення: {user_message}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=message_to_admin)

# Коли адмін відповідає користувачу
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Команда виглядає так: /reply ID_користувача Текст повідомлення
        args = context.args
        target_user_id = int(args[0])
        reply_text = ' '.join(args[1:])

        await context.bot.send_message(chat_id=target_user_id, text=reply_text)
        await update.message.reply_text("Повідомлення успішно надіслано!")

    except Exception as e:
        await update.message.reply_text(f"Помилка: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
