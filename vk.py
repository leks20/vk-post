import os
from json import JSONDecodeError

import requests
from requests import exceptions
from dotenv import load_dotenv

load_dotenv()

vk_token = os.getenv('vk_token')
vk_user_id = os.getenv('vk_user_id')


def post_vk(text, img):

    BASE_URL = 'https://api.vk.com/method/'

    # получение адреса сервера для загрузки фото,
    # передача файла на сервер,
    # возвращается JSON-объект, содержащий объект с полями server, photo, hash
    def send_photo(img):
        method = 'photos.getWallUploadServer'
        URL = os.path.join(BASE_URL, method)
        data = {
            'access_token': vk_token,
            'v': 5.103,
        }
        files = {'file': open(img, 'rb')}
        try:
            request_1 = requests.post(url=URL, params=data)
            url_server = request_1.json()['response']['upload_url']
            request_2 = requests.post(url=url_server, files=files)
            result = request_2.json()
        except KeyError:
            result = 'Ошибка при получении данных из JSON-объекта'
        except JSONDecodeError:
            result = 'Не удалось получить ответ в формате JSON'
        except exceptions.RequestException as e:
            result = f'При попытке соединения возникла следующая ошибка:\n{e}'
        return result

    # сохранение фотографии
    def save_photo(img):
        method = 'photos.saveWallPhoto'
        URL = os.path.join(BASE_URL, method)
        server, photo, hash = [item for item in send_photo(img).values()]
        data = {
            'access_token': vk_token,
            'v': 5.103,
            'server': server,
            'photo': photo,
            'hash': hash,
        }
        try:
            request = requests.post(url=URL, params=data)
            result = request.json()['response'][0]['id']
        except KeyError:
            result = 'Ошибка при получении данных из JSON-объекта'
        except JSONDecodeError:
            result = 'Не удалось получить ответ в формате JSON'
        except exceptions.RequestException as e:
            result = f'При попытке соединения возникла следующая ошибка:\n{e}'
        return result

    # публикация поста с приложением фото
    def post(text, img):
        method = 'wall.post'
        URL = os.path.join(BASE_URL, method)
        owner_id = vk_user_id
        media_id = save_photo(img)
        data = {
            'access_token': vk_token,
            'owner_id': owner_id,
            'message': text,
            'v': 5.103,
            'attachments': f'photo{owner_id}_{media_id}'
        }
        try:
            request = requests.post(url=URL, params=data)
            if request.json()['response']:
                final_message = 'Запись на стене опубликована'
        except KeyError:
            final_message = 'Сообщение об ошибке с сайта VK:\n'+request.json()['error']['error_msg']
        except JSONDecodeError:
            final_message = 'Не удалось получить ответ в формате JSON'
        except exceptions.RequestException as e:
            final_message = f'При попытке соединения возникла следующая ошибка:\n{e}'
        return final_message

    return post(text, img)
