from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from data_base import sql_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from keyboards.admin_kb import button_case_admin


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напиши Привет или Добрый день')


async def any_text(message: types.Message):
    if message.text.lower() == 'привет' or message.text.lower() == 'добрый день':
        await bot.send_message(message.from_user.id, 'Добрый день! Нажми нужную кнопку!',
                               reply_markup=button_case_admin)
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши Привет или Добрый день')


async def my_tasks_command(message: types.Message):
    await sql_db.sql_read(message)


class FSMAdmin(StatesGroup):
    name_task = State()
    date_task = State()
    time_task = State()
    description_task = State()


async def dialog_start(message: types.Message):
    await FSMAdmin.name_task.set()
    await message.reply('Введите название дела')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите дату')


async def enter_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите время')


async def enter_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание дела')


async def enter_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await sql_db.sql_add_command(state)
    await bot.send_message(message.from_user.id, 'Новое дело успешно добавлено!')
    await state.finish()


async def del_callback_run(callback: types.CallbackQuery):
    if callback.data and callback.data.startswith('del '):
        await sql_db.sql_delete_command(callback.data.replace('del ', ''))
        await callback.answer(text=f'{callback.data.replace("del ", "")} удалена.', show_alert=True)


async def delete_item(message: types.Message):
    read = await sql_db.sql_read2()
    for ret in read:
        await bot.send_message(message.from_user.id,
                               f'{ret[0]}\nДата: {ret[1]}\nВремя: {ret[2]}\nОписание: {ret[3]}')
        await bot.send_message(message.from_user.id, 'Удалить из списка дел?', reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(my_tasks_command, commands=['Мои_дела'])
    dp.register_message_handler(dialog_start, commands=['Добавить'], state=None)
    dp.register_message_handler(cancel_handler, commands=['отмена'], state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(enter_name, state=FSMAdmin.name_task)
    dp.register_message_handler(enter_date, state=FSMAdmin.date_task)
    dp.register_message_handler(enter_time, state=FSMAdmin.time_task)
    dp.register_message_handler(enter_description, state=FSMAdmin.description_task)
    dp.register_callback_query_handler(del_callback_run)
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_message_handler(any_text)
