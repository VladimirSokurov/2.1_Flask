import requests

URL = f'http://127.0.0.1:5000/advert/'


def add_advert(title: str, description: str, user_name: str):
    request = requests.post(URL, json={'title': title, 'description': description, 'user_name': user_name})
    print(f'{request.status_code=}')
    print(f'{request.json()=}')


def get_advert(advert_id: str):
    request = requests.get(f'{URL}/{advert_id}/')
    print(f'{request.status_code=}')
    print(f'{request.json()=}')


def delete_advert(advert_id: str):
    request = requests.delete(f'{URL}/{advert_id}/')
    print(f'{request.status_code=}')
    print(f'{request.json()=}')


# add_advert(title='title_1', description='description_1', user_name='user_1')
# add_advert(title='title_2', description='description_2', user_name='user_2')
# add_advert(title='title_3', description='description_3', user_name='user_3')

# get_advert(advert_id='1')
# get_advert(advert_id='2')
# get_advert(advert_id='3')

# delete_advert(advert_id='1')
# delete_advert(advert_id='2')
# delete_advert(advert_id='3')
