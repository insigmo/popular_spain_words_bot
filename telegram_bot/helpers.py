from telegram_bot.db.db_manager import DBManager
from telegram_bot.db.tables import User


async def db_add_or_update_user(user: dict) -> None:
    async with DBManager() as manager:
        await manager.add_or_update_user(user)


async def db_get_users() -> list[User]:
    async with DBManager() as manager:
        return await manager.get_all_users()


async def db_get_known_words(user_id: int) -> list[str]:
    async with DBManager() as manager:
        return await manager.get_known_words_by_user_id(user_id)


async def db_save_words(user_id: int, words: list[str]):
    async with DBManager() as manager:
        return await manager.update_known_words(user_id, words)
