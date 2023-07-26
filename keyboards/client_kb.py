from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Мои_дела')
b2 = KeyboardButton('/Добавить_дело')
b3 = KeyboardButton('/Удалить_дело')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).row(b2, b3)
