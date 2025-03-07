from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv(Path(__file__).parent.parent /'build/.env')


class Settings(BaseSettings):
    BOT_TOKEN: str = Field()
    POSTGRES_USER: str = Field()
    POSTGRES_PASSWORD: str = Field()
    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: str = Field()

SETTINGS = Settings()
# SETTINGS.POSTGRES_HOST = "localhost"

bot = Bot(SETTINGS.BOT_TOKEN)
dp = Dispatcher()
