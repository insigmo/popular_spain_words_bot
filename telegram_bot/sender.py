import asyncio
import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path

import uvloop

from telegram_bot.config import bot
from telegram_bot.db.tables import User
from telegram_bot.helpers import db_get_users, db_get_known_words, db_save_words


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

words_path = Path(__file__).parent / 'all_words.json'
all_words: list[str] = json.loads(words_path.read_text())


async def _send_message(user: User):
    user_known_words = await db_get_known_words(user.id) or []
    words_for_knowing = list(set(all_words) - set(user_known_words))[:user.words_count]
    today_words = {}
    if not words_for_knowing:
        user.enable = False
        await bot.send_message(user.id, textwrap.dedent('Thanks for studying the most popular words'
                                                        'If you memorized all words, you can understand Spanish speach'
                                                        'Hasta Luego!'))
        return

    for word in words_for_knowing:
        user_known_words[word] = all_words[word]
        today_words[word] = all_words[word]

    await db_save_words(user.id, user_known_words)

    today = datetime.now().strftime('%d/%m/%Y')
    words = '\n'.join(f'\t\t\t\t{en}: {ru}' for en, ru in today_words.items())
    msg = (textwrap.dedent(f"""{today}: \n{words}\n"""))

    logger.debug(f'{msg} for {user.first_name}')
    await bot.message.send_message(user.id, textwrap.dedent(msg))


async def main():
    users = await db_get_users()
    for user in users:
        if user.enable and user.what_hour == int(datetime.now().strftime('%H')):
            await _send_message(user)


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main())
