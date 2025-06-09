import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = {"stage": "awaiting_task"}
    await update.message.reply_text("📝 Please enter the task you want to be reminded of:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text
    state = user_states.get(chat_id, {"stage": None})

    if state["stage"] == "awaiting_task":
        user_states[chat_id] = {"stage": "awaiting_time", "task": message}
        await update.message.reply_text("⌛ INPUT RECEIVED.\nSpecify time in minutes (digits only).")

    elif state["stage"] == "awaiting_time":
        try:
            minutes = int(message)
            task = state["task"]
            seconds = minutes * 60
            await update.message.reply_text(
                f"✅ CONFIRMED.\nI will remind you to: “{task}” in {minutes} minute(s)."
            )
            await asyncio.sleep(seconds)
            await context.bot.send_message(chat_id=chat_id, text=f"🔔 REMINDER:\n{task}")
            user_states[chat_id] = {"stage": None}
        except ValueError:
            await update.message.reply_text("⚠️ INVALID INPUT.\nPlease type a number in minutes.")
    else:
        await update.message.reply_text("🛑 COMMAND UNKNOWN.\nUse /start to initiate a reminder sequence.")

async def main():
    application = ApplicationBuilder().token("8150380591:AAEuATLzOvPwN-b4OUY4VCpOI8rSmHPWXbo").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
