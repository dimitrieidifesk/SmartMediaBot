from aiogram.utils import executor
import logging

from src.core.settings import project_settings
from src.core.logging_setup import init_logger
from TelegramBot.bot import *

init_logger()

if __name__ == '__main__':
    logging.info(f'-- Project {project_settings.PROJECT_NAME} {project_settings.PROJECT_VERSION} starting --')
    executor.start_polling(dp)
