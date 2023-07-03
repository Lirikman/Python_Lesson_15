import telebot
from telebot import apihelper
import time

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'

BOT_URL = f'https://api.telegram.org/bot{TOKEN}'

proxies = {
    'http': '221.141.158.183:80',
    'https': '117.251.103.186:8080',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def recieve_text(message):
    text = message.text
    bot.reply_to(message, f'Добрый день! Вы сказали : {text.upper()}')


@bot.message_handler(commands=['start'])
def command_start_function(message):
    bot.reply_to(message, 'Рад Вас приветствовать!')


bot.polling()
