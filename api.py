"""Модуль 19"""
import json
from settings import valid_email, valid_password

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
import time

class ArgumentsException (Exception):
    pass

# текущая дата, чтобы создать лог файлс с таким именем
filename = time.strftime('%Y-%m-%d %H-%M') + '.txt'

class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def debug(func):
        """Выводит сигнатуру функции и возвращаемое значение"""

        def wrapper_debug(*args, **kwargs):


            my_file = open(filename, "a")

            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            my_file.write(f"Информация по вызываемой функции api запроса: \n")
            print(f"\nНазвание функции: {func.__name__}({signature})\n")
            my_file.write(f"Название функции: {func.__name__}({signature})"+ '\n')
            print(f"сигнатура функции: {signature}\n")
            my_file.write(f"сигнатура функции: {signature}"+ '\n')
            print(f"аргументы: {args_repr}\n")
            my_file.write(f"аргументы: {args_repr}" + '\n')
            my_file.write("***************************************************** \n")
            # my_file.close()
            value = func(*args, **kwargs)
            # print(f"{func.__name__!r} вернула значение - {value!r} \n")
            # my_file.write(f"{func.__name__!r} вернула значение - {value!r}" + '\n')
            my_file.write("***************************************************** \n")
            my_file.close()
            return value

        return wrapper_debug

    @debug
    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': passwd,
        }

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"URL: {self.base_url+'api/key'}" + '\n')

        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    @debug
    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"params: {filter})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/pets/'}" + '\n')

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @debug
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # ссылаемся на файл
        my_file = open(filename, "a")

        # Задаем диапазон валидных значений возраста
        if len(age) != 0:
            if int(age) <0 or int(age)>100:
                my_file.write(f"возраст питомца может быть в диапазоне от 0 до 100 лет" + '\n')
                raise  ArgumentsException("возраст питомца может быть в диапазоне от 0 до 100 лет")
        if age =='':
            my_file.write(f"возраст не может быть пустым" + '\n')
            raise ArgumentsException("возраст не может быть пустым")
        if name == '':
            my_file.write(f"имя не может быть пустым" + '\n')
            raise ArgumentsException("имя не может быть пустым")
        if animal_type == '':
            my_file.write(f"порода не может быть пустой" + '\n')
            raise ArgumentsException("порода не может быть пустой")

        for i in range(33, 65):
            if chr(i) in name:
                my_file.write(f"имя не может содержать спецсимволы" + '\n')
                raise ArgumentsException("имя не может содержать спецсимволы")
                break
        for i in range(91, 97):
            if chr(i) in name:
                my_file.write(f"имя не может содержать спецсимволы" + '\n')
                raise ArgumentsException("имя не может содержать спецсимволы")
                break

        for i in range(33, 65):
            if chr(i) in animal_type:
                my_file.write(f"вид животного не может содержать спецсимволы" + '\n')
                raise ArgumentsException("вид животного не может содержать спецсимволы")
                break
        for i in range(91, 97):
            if chr(i) in animal_type:
                my_file.write(f"вид животного не может содержать спецсимволы" + '\n')
                raise ArgumentsException("вид животного не может содержать спецсимволы")
                break
        if name[0] == ' ':
            my_file.write(f"имя животного не может начинаться с пробела" + '\n')
            raise ArgumentsException("имя животного не может начинаться с пробела")
        if animal_type[0] == ' ':
            my_file.write(f"вид животного не может начинаться с пробела" + '\n')
            raise ArgumentsException("вид животного не может начинаться с пробела")



        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}


        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"data: {data})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/pets'}" + '\n')

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    @debug
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/pets/'}" + '\n')


        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @debug
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"data: {data})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/pets/'}" + '\n')

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @debug
    def add_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце (без фото) и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"data: {data})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/create_pet_simple'}" + '\n')


        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    @debug
    def add_photo_to_pet_without_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемой фотографии питомца и возвращает статус
        запроса на сервер и результат в формате JSON """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        my_file = open(filename, "a")
        my_file.write(f"headers: {headers})" + '\n')
        my_file.write(f"URL: {self.base_url + 'api/pets/set_photo/'}" + '\n')
        my_file.write(f"data: {data})" + '\n')

        res = requests.post(self.base_url +'api/pets/set_photo/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

# pf = PetFriends()
# status, key = pf.get_api_key(valid_email, valid_password)
# print(status)
# print(key)
# # key['key'] = ''
# print("********************************************************")
# pet_photo = 'tests/images/cat1.jpg'
# status, result = pf.add_new_pet(key, 'Artur', 'кот', '5', pet_photo)
# print(status)
# print(result)
# print("********************************************************")
# status, result = pf.add_pet_without_photo(key, 'Avanes', 'human', '38')
# print(status)
# print(result)
# print(f"ID элемента без фото {result['id']}")
# print("********************************************************")
# id = result['id']
# print(type(id))
# photo = 'tests/images/rudik.jpg'
# status, result = pf.add_photo_to_pet_without_photo(key, id,photo)
# print(status)
# print(result)
# print(f"ID элемента, которому добавили фото {result['id']}")
# print("********************************************************")
# # status, result = pf.delete_pet(key, id)
# # print(status)
# # print(result)