import telebot
from utils import ConvertionException, Converter
from config import keys, key_cbr, TOKEN

bot = telebot.TeleBot(token = TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Привет! Я бот - конвертатор валют \n " \
"Я работаю по курсам ЦБ РФ \n" \
"При конвертациях не в рублях расчет идет по кросс-курсу через рубль \n" \
"Для расчета конвертации напиши сообщение в формате: \n " \
"<имя валюты> <в какую перевести> <кол-во вылюты> \n " \
"Увидеть список доступных валют - /values"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in key_cbr.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")
        quote, base, amount = values
        total_base = Converter.do_convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, "Не удалось обработать команду")
    else:
        text = f'Цена {amount} {quote} в {base} - {round(total_base, 3)}'
        bot.send_message(message.chat.id, text)

bot.polling()
