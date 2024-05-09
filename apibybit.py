import time
import hmac
import hashlib
import requests

# Функция для отправки запроса на создание ордера
def create_order(api_key, api_secret, symbol, side, quantity, price):
    BASE_URL = 'https://api.bybit.com'
    ENDPOINT = '/v2/private/order/create'

    payload = {
        'api_key': api_key,
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'order_type': 'Limit',
        'time_in_force': 'GoodTillCancel',
    }

    query_string = '&'.join([f"{key}={value}" for key, value in sorted(payload.items())])
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    payload['sign'] = signature

    response = requests.post(BASE_URL + ENDPOINT, data=payload)

    if response.status_code == 200:
        print(f"Ордер для аккаунта {api_key} успешно размещен.")
        print("ID ордера:", response.json()['result']['order_id'])
        with open('order_result.txt', 'a') as f:
            f.write(f"Order Params1 Completed\n")
    else:
        print(f"Ошибка для аккаунта {api_key}:", response.json()['ret_msg'])

# Функция для выполнения покупки один раз в указанное время
def execute_trade_once(api_key, api_secret, symbol, side, quantity, price, execution_time):
    current_time = time.time()
    time_to_wait = execution_time - current_time
    if time_to_wait > 0:
        print(f"Ожидание времени выполнения: {execution_time}")
        time.sleep(time_to_wait)
    create_order(api_key, api_secret, symbol, side, quantity, price)

# Параметры для вашего аккаунта
account_params = {
    'api_key': 'gX4h9qSm4VZF3LHRrr',
    'api_secret': 'l3PD8cn0rb57BtmrpiAiLhHVQAO7e9ZXlzKA',
    'symbol': 'BRETTUSDT',
    'side': 'Buy',
    'quantity': 24,  # Количество BRETT для покупки
    'price': 0.039,  # Цена покупки в USDT
    'execution_time': time.mktime(time.strptime('2024-05-10 21:30:00', '%Y-%m-%d %H:%M:%S'))  # Время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС UTC
}

# Выполнение покупки один раз в указанное время
execute_trade_once(
    account_params['api_key'],
    account_params['api_secret'],
    account_params['symbol'],
    account_params['side'],
    account_params['quantity'],
    account_params['price'],
    account_params['execution_time']
)
