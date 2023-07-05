import telebot
from telebot import apihelper
import time

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'

proxies = {
    'http': '221.141.158.183:80',
    'https': '117.251.103.186:8080',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start_function(message):
    bot.reply_to(message, 'Рад Вас приветствовать!')


@bot.message_handler(commands=['admin'], func=lambda message: message.from_user.id == 5361274567)
def admin(message):
    print(message)
    bot.reply_to(message, 'Добрый день, хозяин!')


@bot.message_handler(commands=['admin_'])
def admin_(message):
    if (message.from_user.id == 5361274567):
        bot.reply_to(message, 'Добрый день, хозяин!')
    else:
        bot.reply_to(message, 'Ты не мой хозяин!')

@bot.message_handler(content_types=['text'])
def recieve_text(message):
    text = message.text
    bot.reply_to(message, f'Добрый день! Вы сказали : {text.upper()}')


bot.polling()
