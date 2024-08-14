from environs import Env
import logging
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from dialogflow import df_response
from tg_logger import TelegramLogsHandler

logger = logging.getLogger("tg bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Вы можете задать мне вопрос, и я постараюсь ответить."
    )


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.message.text
        chat_id = update.effective_chat.id

        answer, _ = df_response(
            context.bot_data["project_id"],
            chat_id,
            query,
            "ru",
        )
    except Exception:
        logger.error(f"exception while replying: to {query} in {chat_id}")
        answer = "Произошла ошибка, попробуйте повторить вопрос"
    logger.error(f"message {answer}")

    await update.message.reply_text(answer)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")

    credentials_path = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        logger.error("Please set path to credentials.json in .env")
        return

    with open(credentials_path, "r") as f:
        credentials = json.load(f)

    if not credentials:
        logger.error("Bad credentials.json file")
        return

    if tg_log_chat_id := env.str("TG_LOGS_CHAT_ID", None):
        tg_handler = TelegramLogsHandler(tg_token, tg_log_chat_id)
        logger.addHandler(tg_handler)

    support_bot = Application.builder().token(tg_token).build()
    support_bot.bot_data["project_id"] = credentials["project_id"]
    support_bot.add_handler(CommandHandler("start", start))
    support_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user)
    )
    support_bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
