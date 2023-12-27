import json
import os
from datetime import datetime
import requests

API_KEY: str = os.getenv('EXCHANGERATES_DATA_API')


def get_currency_rate(currency: str) -> dict:
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    payload = {}
    headers = {"apikey": API_KEY}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    data = {"currency": currency, "rate": response_data["rates"]["RUB"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    print(data)
    return data

def save_to_json(data: dict, file_json) -> None:
    """Проверяем информацию по курсу в json файле, если курс поменялся, то перезаписываем новым курсом"""
    if not os.path.isfile(file_json):
        with open(file_json, "w") as write_file:
            json.dump(data, write_file)
    else:
        with open(file_json, "r") as read_file:
            data_dict = json.load(read_file)
            if data_dict.get("rate") != data.get("rate"):
                with open(file_json, "w") as overwrite_file:
                    json.dump(data, overwrite_file)

def get_read_json(file_json):
    """Вычитываем данные из json файла"""
    with open(file_json, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data
