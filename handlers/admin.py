from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot

ID = None


class FSMAdmin(StatesGroup):
    name_task = State()
    date_task = State()
    time_task = State()
    description_task = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Приветствую хозяин!')
    await message.delete()


async def dialog_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name_task.set()
        await message.reply('Введите название дела')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


async def enter_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите дату')


async def enter_date(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['date'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите время')


async def enter_time(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['time'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание дела')


async def enter_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        async with state.proxy() as data:
            await message.reply(str(data))
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(dialog_start, commands=['Начало'], state=None)
    dp.register_message_handler(cancel_handler, commands=['отмена'], state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(enter_name, state=FSMAdmin.name_task)
    dp.register_message_handler(enter_date, state=FSMAdmin.date_task)
    dp.register_message_handler(enter_time, state=FSMAdmin.time_task)
    dp.register_message_handler(enter_description, state=FSMAdmin.description_task)
    dp.register_message_handler(make_changes_command, commands=['moderator'])
