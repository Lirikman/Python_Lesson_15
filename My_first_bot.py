from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import sqlite3 as sq

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Бот онлайн')
    sql_start()

b1 = KeyboardButton('/Дела')
b2 = KeyboardButton('/Добавить')
b3 = KeyboardButton('/Удалить')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.add(b1).row(b2, b3)

base = sq.connect('my_task.db')
cur = base.cursor()


def sql_start():
    global base, cur
    if base:
        print('База данных успешно подключена!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT, date TEXT, time TEXT, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напиши Привет или Добрый день')


@dp.message_handler(commands=['Дела'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Список дел пуст!')


#@dp.message_handler(commands=['Добавить'])
#async def command_start(message: types.Message):
#    await bot.send_message(message.from_user.id, 'Дело успешно добавлено!')


@dp.message_handler(commands=['Удалить'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Дело успешно удалено!')


class FSMBot(StatesGroup):
    name = State()
    date = State()
    time = State()
    description = State()


@dp.message_handler(commands='Добавить', State=None)
async def add_tasks(message: types.Message):
    await FSMBot.name.set()
    await message.reply('Введи название дела!')


@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state=FSMBot.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMBot.next()
    await message.reply('Введи планируемую дату')


@dp.message_handler(state=FSMBot.date)
async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMBot.next()
    await message.reply('Введи планируемое время')


@dp.message_handler(state=FSMBot.time)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await FSMBot.next()
    await message.reply('Введи описание дела')


@dp.message_handler(state=FSMBot.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMBot.next()
    await sql_add_command(state)
    await message.answer('Дело успешно добавлено!')

    await state.finish()


@dp.message_handler()
async def any_text(message: types.Message):
    if message.text.lower() == 'привет' or message.text.lower() == 'добрый день':
        await bot.send_message(message.from_user.id, 'Добрый день! Нажми нужную кнопку', reply_markup=kb)
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши Привет или Добрый день')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
