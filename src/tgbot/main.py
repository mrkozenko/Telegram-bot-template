import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fluent.runtime import FluentResourceLoader, FluentLocalization

from src.tgbot.config import load_config
from src.tgbot.handlers.user import router as user_router
from src.tgbot.middlewares.l10n import L10nMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config("bot.ini")

    storage = MemoryStorage()
    locales_dir = Path(__file__).parent.joinpath("locales")

    l10n_loader = FluentResourceLoader(str(locales_dir) + "/{locale}")
    l10n = FluentLocalization(["uk"], ["strings.ftl", "errors.ftl"], l10n_loader)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)

    dp.update.middleware(L10nMiddleware(l10n))
    # start
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
