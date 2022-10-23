import pytest
import requests
from settings import valid_email, valid_password

@pytest.fixture(scope="session", autouse=True)
def auth_key(email=valid_email, passwd=valid_password):
    """Фикстура делает запрос к API сервера и возвращает статус запроса и результат в формате
            JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
    base_url = "https://petfriends.skillfactory.ru/"
    headers = {
        'email': email,
        'password': passwd,
    }
    res = requests.get(base_url + 'api/key', headers=headers)
    status = res.status_code
    result = ""
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return result
    # return status, result