import logging
import asyncio
import telegram


class TelegramLogsHandler(logging.Handler):
    """Handler for sending messages via telegram bot."""

    def __init__(self, token: str, chat_id: str) -> None:
        """Inits bot and chat id."""
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=token)

    def emit(self, record: logging.LogRecord) -> None:
        """Sends logger message to bot."""
        log_entry = self.format(record)

        loop = asyncio.get_running_loop()

        asyncio.run_coroutine_threadsafe(
            self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry), loop
        )
