import json
import os
import requests

API_KEY: str = os.getenv('EXCHANGERATES_DATA_API')


def get_currency_rate(currency: str) -> float:
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    payload = {}
    headers = {"apikey": API_KEY}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def save_to_json(data: dict, file_json) -> None:
    """Сохраняет данные в json файл"""
    with open(file_json, "a") as f:
        if os.stat(file_json).st_size == 0:
            json.dump([data], f)
        else:
            with open(file_json) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(file_json, "w") as json_file:
                json.dump(data_list, json_file)


def get_read_json(file_json):
    """Вычитываем данные из json файла"""
    with open(file_json, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data
