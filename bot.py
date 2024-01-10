# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

import telebot
from telebot import types

import datetime
import logging

from ImageMaker import ImageMaker
from WeatherAPI import WeatherMaker

"""
Бот позволяющий получить данные о погоде в приложении Telegram.
Use python 3.11

Поддерживает ответы на запросы:
    - узнать погоду на данный момент;
    - узнать погоду на ближайшие 5 дней;
    - получить изображение, отображающее погоду и данные о ней.
Так же может вывести информацию о своем функционале и стереть все сообщения из чата.
"""

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

log = logging.getLogger('weather_bot')


def configure_logging():
    """Шаблоны логирования для консольной и файловой записи."""
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename='weather_bot.log', encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message):
    """Дает первичные указания пользователю для начала работы."""
    bot.send_message(message.chat.id, 'Напишите название города в котором хотите узнать погоду.')


@bot.message_handler(commands=['help'])
def help(message):
    """Предоставляет пользователю информацию о функционале бота."""
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.row(btn1)
    btn2 = types.KeyboardButton('/help')
    btn3 = types.KeyboardButton('/delete')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Это специальный бот для поиска погоды. У него есть следующие команды: \n"
                                      "/start -- основная команда позволяющая узнать: \n"
                                      "    - погоду на данный момент времени;\n"
                                      "    - погоду на пять дней вперед;\n"
                                      "    - получить открытку с погодой на данный момент времени.\n"
                                      "/help -- выводит информацию о функционале бота "
                                      "(если вы это читаете, значит вы уже находитесь в ней ;).\n"
                                      "/delete -- полностью чистит чат от сообщений.\n"
                                      "\n"
                                      "Готовы узнать погоду?",
                     reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete_all_message(message):
    """Удаляет все сообщения из чата, очищая его."""
    try:
        n = 0
        while message:
            bot.delete_message(message.chat.id, message.message_id - n)
            n += 1
    except Exception:
        log.debug('Чат с пользователем был очищен.')


@bot.message_handler(content_types=['text'])
def get_choice(message):
    """
    Функция, запрашивающая у пользователя название города и предоставляющая выбор пользователю:
    - узнать погоду на данный момент;
    - узнать погоду на ближайшие 5 дней;
    - получить изображение, отображающее погоду и данные о ней.
    """
    global choice, user
    user = message.from_user
    choice = message.text
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Узнать погоду на сегодня', callback_data='w_today')
    btn2 = types.InlineKeyboardButton('Узнать погоду на 5 дней', callback_data='w_five_day')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Получить открытку', callback_data='image')
    markup.row(btn3)
    bot.reply_to(message, f'Погода в городе {choice}:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    """Функция обработки выбора, сделанного пользователем."""
    try:
        if callback.data == 'w_today':
            weather = WeatherMaker()
            weather_today = weather.search_weather_now(choice)
            message_out = (
                f'Дата: {weather_today["date"]}, температура воздуха: {weather_today["temp"]} градусов цельсия, '
                f'{weather_today["weather"]}, ветер: {weather_today["wind"]} м/с, город: {weather_today["city"]}.')
            bot.send_message(callback.message.chat.id, message_out)
            log.debug(f'Пользователь {user.first_name} {user.last_name} '
                      f'сделал запрос погоды на данный момент ({datetime.datetime.now()}).')
        elif callback.data == 'w_five_day':
            weather = WeatherMaker()
            weather_five_day = weather.search_weather(choice)
            for w in weather_five_day:
                message_out = (
                    f'Дата: {w["date"]}, температура воздуха: {w["temp"]} градусов цельсия, '
                    f'{w["weather"]}, ветер: {w["wind"]} м/с, город: {w["city"]}.')
                bot.send_message(callback.message.chat.id, message_out)
            log.debug(f'Пользователь {user.first_name} {user.last_name} '
                      f'сделал запрос погоды на 5 дней вперед, начиная с {datetime.datetime.now()}.')
        elif callback.data == 'image':
            weather = WeatherMaker()
            weather_data = weather.search_weather_now(choice)
            show_weather = ImageMaker(weather_data)
            show_weather.image_make()
            file = open('./result.jpg', 'rb')
            bot.send_photo(callback.message.chat.id, file)
            log.debug(f'Пользователь {user.first_name} {user.last_name} '
                      f'сделал запрос изображения с погодой на {datetime.datetime.now()}.')
    except Exception:
        bot.send_message(callback.message.chat.id, 'Произошла ошибка, возможно вы ввели неправильный город. '
                                                   'Попробуйте еще раз.')
        log.info('Ввод некорректных данных от пользователя.')


if __name__ == '__main__':
    """Запуск бота."""
    configure_logging()
    bot.polling(none_stop=True, interval=0)
