from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

kb = ReplyKeyboardMarkup(resize_keyboard=True) #one_time_keyboard=True)
kb.add(b1).row(b2, b3)

base = sq.connect('my_task.db')
cur = base.cursor()


def sql_start():
    global base, cur
    if base:
        print('База данных успешно подключена!')
    base.execute('CREATE TABLE IF NOT EXISTS tasks(name TEXT, date TEXT, time TEXT, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO tasks VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_delete_command(data):
    cur.execute('DELETE FROM tasks WHERE name == ?', (data,))
    base.commit()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback: types.CallbackQuery):
    await sql_delete_command(callback.data.replace('del ', ''))
    await callback.answer(text=f'{callback.data.replace("del ", "")} удалена.', show_alert=True)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напиши Привет или Добрый день')


@dp.message_handler(commands=['Дела'])
async def command_start(message: types.Message):
    for ret in cur.execute('SELECT * FROM tasks').fetchall():
        await bot.send_message(message.from_user.id, (f'Задача: {ret[0]}\nДата: {ret[1]}\n'
                                                      f'Время: {ret[2]}\nОписание: {ret[3]}'))


@dp.message_handler(commands=['Удалить'])
async def command_delete(message: types.Message):
    for ret in cur.execute('SELECT * FROM tasks').fetchall():
        await bot.send_message(message.from_user.id, (f'Задача: {ret[0]}\nДата: {ret[1]}\n'
                                                      f'Время: {ret[2]}\nОписание: {ret[3]}'))
        await bot.send_message(message.from_user.id, text='^^^ ВЫ ХОТИТЕ УДАЛИТЬ ЭТО ДЕЛО? ^^^',
                               reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


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
