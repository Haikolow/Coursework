import requests
import json
import time
from tqdm import tqdm

def get_photos_vk(user_id, access_token):
    params = {
        'user_id': user_id,
        'access_token': access_token,
        'v': '5.131',
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1
    }
    response = requests.get('https://api.vk.com/method/photos.get', params=params)
    response_json = response.json()
    photos = response_json['response']['items']
    return photos
def upload_photos_yandex_disk(photos, access_token):
    headers = {
        'Authorization': 'OAuth ' + access_token
    }
    folder_name = 'Резервное копирование фотографий с ВК'
    params = {
        'path': folder_name,
        'overwrite': 'true'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers, params=params)
    uploaded_photos = []
    for photo in photos:
        photo_url = photo['sizes'][-1]['url']
        photo_likes = photo['likes']['count']
        photo_name = str(photo_likes) + '.jpg'
        params = {
            'url': photo_url,
            'path': folder_name + '/' + photo_name
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,
                                 params=params)
        uploaded_photos.append({
            'file_name': photo_name,
            'size': photo['sizes'][-1]['type']
        })
    return uploaded_photos
def save_photos_info(photos_info):
    with open('photos_info.json', 'w') as file:
        json.dump(photos_info, file)
def backup_photos_vk_to_yandex_disk(user_id, vk_token, yandex_disk_token, num_photos=5):
    photos = get_photos_vk(user_id, vk_token)
    for j in tqdm(photos):
        time.sleep(1)
    print('Фотографии с профиля пользователя VK получены')
    sorted_photos = sorted(photos, key=lambda photo: photo['likes']['count'], reverse=True)
    for i in tqdm(sorted_photos):
        time.sleep(1)
    print('Сортировка фотографий завершена')
    selected_photos = sorted_photos[:num_photos]
    uploaded_photos = upload_photos_yandex_disk(selected_photos, yandex_disk_token)
    for q in tqdm(uploaded_photos):
        time.sleep(1)
    print('Загрузка фотографий на Яндекс Диск завершена завершена')
    save_photos_info(uploaded_photos)

user_id =  input('Введите id пользователя VK: ')
vk_token = input('Введите токен VK: ')
yandex_disk_token = input('Введите токен Яндекс.Диска: ')

backup_photos_vk_to_yandex_disk(user_id, vk_token, yandex_disk_token)
