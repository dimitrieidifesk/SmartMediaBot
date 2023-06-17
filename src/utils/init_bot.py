from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from src.core.settings import project_settings

bot = Bot(token=project_settings.TOKEN)
dp = Dispatcher(bot)