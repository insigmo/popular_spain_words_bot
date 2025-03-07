import asyncio
import logging

import aioschedule
import uvloop

from telegram_bot.config import bot, dp
from telegram_bot.main import main_router


async def main() -> None:
    dp.include_router(main_router)
    await dp.start_polling(bot)


def _prepare() -> None:
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    _prepare()
    try:
        aioschedule.every().day.at("10:30").do(main)
        # asyncio.run(aioschedule.run_pending())
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
