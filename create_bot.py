from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
