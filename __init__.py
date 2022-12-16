from config import botToken
from aiogram import Bot
import logging
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token=botToken)
dp = Dispatcher(bot, storage=MemoryStorage())