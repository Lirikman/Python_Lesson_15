import telebot
from telebot import apihelper
from telebot import types
import time

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'

proxies = {
    'http': '221.141.158.183:80',
    'https': '117.251.103.186:8080',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'добрый день':
        bot.send_message(message.from_user.id, 'Привет! Давай посмотрим на список твоих дел!')
        keyboard = types.InlineKeyboardMarkup()
        key_tasks = types.InlineKeyboardButton(text = 'Список всех дел', callback_data='tasks')
        keyboard.add(key_tasks)
        key_add_task = types.InlineKeyboardButton(text='Добавить новую задачу', callback_data='add_task')
        keyboard.add(key_add_task)
        key_remove_task = types.InlineKeyboardButton(text='Удалить задачу', callback_data='remove_task')
        keyboard.add(key_remove_task)
        bot.send_message(message.from_user.id, text='Выбери нужную кнопку', reply_markup=keyboard)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши Привет или Добрый день')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши Привет или Добрый день')


bot.polling()
