import os
from datetime import datetime
import telebot
from telebot import types
from currency import get_currency_rate, get_read_json, save_to_json

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


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "USD":
        currency = "USD"
        file_json = "currency_rates_usd.json"
    elif call.data == "EUR":
        currency = "EUR"
        file_json = "currency_rates_eur.json"
    rate = get_currency_rate(currency)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"currency": currency, "rate": rate, "timestamp": timestamp}
    save_to_json(data, file_json)
    read_json = get_read_json(file_json)
    count_req = len(read_json)
    if count_req == 1:
        rate = read_json[0].get("rate")
        bot.send_message(call.message.chat.id, f"Курс рубля к {currency} на текущий момент {rate:.2f}")
    if count_req > 1:
        last_rate = read_json[-1].get("rate")
        prelast_rate = read_json[-2].get("rate")
        if last_rate > prelast_rate:
            bot.send_message(call.message.chat.id,
                             f"После предыдущего запроса курс рубля к {currency} упал, на текущий момент равен {rate:.2f}")
        elif last_rate < prelast_rate:
            bot.send_message(call.message.chat.id,
                             f"После предыдущего запроса курс рубля к {currency} вырос, на текущий момент равен {rate:.2f}")
        elif last_rate == prelast_rate:
            bot.send_message(call.message.chat.id,
                             f"После предыдущего запроса курс рубля к {currency} не поменялся {rate:.2f}")

# Запускаем бота
bot.polling(none_stop=True, interval=0)
