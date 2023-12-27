import os
import time
import telebot
from telebot import types
from currency_time import get_currency_rate, save_to_json, get_read_json

API_KEY: str = os.getenv('TOKEN_TELEGRAM')

# Создаем экземпляр бота
bot = telebot.TeleBot(API_KEY)

# Команда start, созание клавиатуры и кнопок
@bot.message_handler(commands=['start'])
def start_message(message):
    currencybutton = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_usd = types.InlineKeyboardButton("USD", callback_data='USD')
    button_eur = types.InlineKeyboardButton("EUR", callback_data='EUR')
    currencybutton.add(button_usd, button_eur)
    bot.send_message(message.chat.id, 'Нажми кнопку с названием валюты чтобы узнать текущий курс к рублю',
                     reply_markup=currencybutton)

# Передача курса в бот каждую минуту
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global currency, file_json
    while True:
        if call.data == "USD":
            currency = "USD"
            file_json = "currency_rates_usd.json"
        elif call.data == "EUR":
            currency = "EUR"
            file_json = "currency_rates_eur.json"
        data = get_currency_rate(currency)
        rate = data.get("rate")
        if not os.path.isfile(file_json):
            bot.send_message(call.message.chat.id, f"Курс рубля к {currency} на текущий момент {rate}")
            save_to_json(data, file_json)
        else:
            read_json = get_read_json(file_json)
            if rate == read_json.get("rate"):
                bot.send_message(call.message.chat.id,
                                 f"После предыдущего запроса курс рубля к {currency} не поменялся {rate}")
            elif rate < read_json.get("rate"):
                bot.send_message(call.message.chat.id,
                                 f"После предыдущего запроса курс рубля к {currency} вырос, на текущий момент равен {rate}")
                save_to_json(data, file_json)
            elif rate > read_json.get("rate"):
                bot.send_message(call.message.chat.id,
                                 f"После предыдущего запроса курс рубля к {currency} упал, на текущий момент равен {rate}")
                save_to_json(data, file_json)
        time.sleep(60)


# Запуск бота
bot.polling(none_stop=True, interval=0)
