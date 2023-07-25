from aiogram import types, Dispatcher
from create_bot import bot


async def command_start(message: types.Message):
    if message.text == '/help' or message.text == '/start':
        await bot.send_message(message.from_user.id, 'Напиши Привет или Добрый день')
    elif message.text.lower() == 'привет' or message.text.lower() == 'добрый день':
        await bot.send_message(message.from_user.id, 'Добрый день! Нажми нужную кнопку!')
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши Привет или Добрый день')


async def command_tasks(message: types.Message):
    await bot.send_message(message.from_user.id, 'Список запланированных дел, пуст!')


async def add_tasks(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы успешно добавили новое дело!')


async def remove_tasks(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбранное дело успешно удалено!')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'Привет', 'Добрый день'])
    dp.register_message_handler(command_tasks, commands=['Мои_дела'])
    dp.register_message_handler(add_tasks, commands=['Добавить_дело'])
    dp.register_message_handler(remove_tasks, commands=['Удалить_дело'])
