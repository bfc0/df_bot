from environs import Env
import logging
from logging.handlers import SysLogHandler
import json
from dialogflow import df_response
from tg_logger import TelegramLogsHandler
from vkbottle.bot import Bot


logger = logging.getLogger("vk bot")


async def reply_to_user(project_id, message):
    user_id = None
    try:
        user_id = message.from_id
        response, is_default = df_response(project_id, user_id, message.text, "ru")

        if is_default:
            return

        await message.answer(response)
    except Exception as e:
        logger.error(f"exception triggered while replying to {user_id}: {e}")


def main():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for l in loggers:
        l.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    logger.addHandler(SysLogHandler(address="/dev/log"))

    env = Env()
    env.read_env()
    vk_token = env.str("VK_TOKEN", None)
    if not vk_token:
        logger.error(".env must contain VK_TOKEN")

    credentials_path = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        logger.error("Please set path to credentials.json in .env")

    with open(credentials_path, "r") as f:
        credentials = json.load(f)

    if not (project_id := credentials.get("project_id")):
        logger.error("credentials.json must contain a valid project_id")
        return

    tg_logs_chat_id = env.str("TG_LOGS_CHAT_ID")
    tg_token = env.str("TG_TOKEN")
    if tg_logs_chat_id and tg_token:
        logging.info("init logger")
        tg_handler = TelegramLogsHandler(tg_token, tg_logs_chat_id)
        logger.addHandler(tg_handler)

    bot = Bot(vk_token)
    bot.on.message()(lambda message: reply_to_user(project_id, message))
    bot.run_forever()


if __name__ == "__main__":
    main()
