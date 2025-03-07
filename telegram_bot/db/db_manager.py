import asyncio

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from telegram_bot.config import SETTINGS
from telegram_bot.db.compressor import Compressor
from telegram_bot.db.tables import Base, KnownWords, User

cmp = Compressor()


class DBManager:
    async def __aenter__(self):
        url = (f"postgresql+asyncpg://{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@"
               f"{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}")
        self._engine = create_async_engine(url, echo=True, )
        self._a_session = async_sessionmaker(self._engine, expire_on_commit=False)
        await self._init_models()
        return self

    async def _init_models(self):
        async with self._engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def __aexit__(self, *args, **kwargs):
        await self._engine.dispose()

    async def update_known_words(self, user_id: int, known_words: dict[str, str]) -> None:
        async with self._a_session() as session:
            known_words = cmp.compress(known_words)
            print(f"Updating known words for user {user_id}: {known_words}")

            stmt = update(KnownWords).filter_by(user_id=user_id).values(words=known_words)
            print(stmt.compile())

            await session.execute(stmt)
            await session.commit()

    async def add_or_update_user(self, user: dict) -> None:
        async with self._a_session() as session:
            if await self.get_user_by_user_id(user['id']):
                stmt = update(User).where(User.id == user['id']).values(**user)
                await session.execute(stmt)
                await session.commit()
                return
            user.pop('last_name', None)
            user_table = User(**user)
            session.add(user_table)
            await session.commit()

            known_words_table = KnownWords(user_id=user['id'], words=cmp.compress(b''))
            session.add(known_words_table)
            await session.commit()

    async def get_known_words_by_user_id(self, user_id: int) -> Result:
        async with self._a_session() as session:
            statement = select(KnownWords).where(KnownWords.user_id == user_id)   # type: ignore
            result = (await session.execute(statement)).scalar()
            return cmp.decompress(result.words)

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        async with self._a_session() as session:
            result = await session.get(User, user_id)
            return result

    async def get_all_users(self) -> list[User]:
        async with self._a_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()    # type: ignore


async def main():
    async with DBManager() as manager:
        user_values = {
            'first_name': 'b',
            'id': 161533571,
            'is_bot': False,
            'language_code': 'en',
            'words_count': 10,
            'what_hour': 9,
            'username': 'igmo'
        }

        known_words = {
            "the": "определенный артикль",
            "be": "быть, нужно, будь",
            "and": "и",
            "of": "показывает принадлежность",
            "a/an": "неопределённый артикль"
        }
        await manager.add_or_update_user(user_values)
        await manager.update_known_words(user_values['id'], known_words)
        print(await manager.get_all_users())
        print(await manager.get_known_words_by_user_id(user_values['id']))


if __name__ == '__main__':
    asyncio.run(main())
