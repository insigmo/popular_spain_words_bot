import re
import textwrap

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from telegram_bot.helpers import db_add_or_update_user

main_router = Router()

@main_router.message(Command('start'), Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(textwrap.dedent(
        """
        Бот для изучения 3000 самых популярных английских слов.
        Начните сегодня изучать, например, по 10 слов в день и за 10 месяцев выучите все слова
        Вам станут доступны 95% текстов общей тематики, а остальные 5% вы поймёте интуитивно. Успехов в изучении!
        Для начала нажмите или введите /go_study
        
        Вам доступны следующие команды:
            /start - запуск бота
            /go_study -- запуск обучения или возобновление обучения
            /unsubscribe -- отписаться от ежедневного изучения слов
        """
    ))


@main_router.message(Command('go_study'))
async def go_study(message: types.Message) -> None:
    await message.answer(textwrap.dedent(
        '''
        Отлично! Теперь вы будете получать небольшими порциями слова по 1 тематике. 
        Во сколько хотите получать слова? Напишите /change_time 9 или /change_time 21
        Оповещения будут приходить в 9 утра или в 9 вечера соответственно
        '''))


@main_router.message(Command('unsubscribe'))
async def unsubscribe(message: types.Message) -> None:
    message.from_user.values['enable'] = False
    await db_add_or_update_user(message.from_user.values)

    await message.answer('Вы были отписаны от ежедневного обучения слов. \n'
                         'Для возобновления нажмите или введите /go_study')


@main_router.message(F.text.startswith("/change_time"))
async def change_time(message: types.Message) -> None:
    hour = re.findall(r'\d+', message.text)
    if not hour:
        await message.reply('Извините, но вы не ввели в какой час времени хотите получать уведомления.\n'
                            'Пожалуйста введите "/change_time <hour>" без кавычек. Например /change_time 13')
        return

    hour = int(hour[0])
    data = message.from_user.values[:]
    data['what_hour'] = hour
    await db_add_or_update_user(message.from_user.values)

    await message.answer(f'Вы теперь будете получать уведомления в {hour} часов. \nСчастливого вам дня!')


@main_router.message()
async def add_user(message: Message):
    words_count = int(re.match(r'\w{1,2}', message.text).group())
    user_data = message.from_user

    user_data.values['words_count'] = words_count
    user_data.values['what_hour'] = 9
    user_data.values['enable'] = True

    await db_add_or_update_user(user_data.values)
    await message.answer('Вы были подписаны на ежедневное обучение наиболее используемых английских слов. \n'
                         f'Каждый день в 9 утра вы будете получать по {words_count} слов.\n'
                         'Если вы хотите выбрать другое время оповещения в 24-часовом формате, '
                         'введите "/change_time <hour>" без кавычек. Например /change_time 13')
