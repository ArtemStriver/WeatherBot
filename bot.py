import telebot
from settings import TOKEN
"""
Бот выдающий погоду на ближайшие 5 дней.
Use python 3.11
"""


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def run():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run()
