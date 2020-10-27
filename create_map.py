import json

from time import time

import requests


BASE_URL = 'https://aspectum.com'
EXTERNAL_API_URL = f'{BASE_URL}/external-api/v1'
API_URL = f'{BASE_URL}/api/v1'

TOKEN = ''
HEADERS = {
    'authorization': f'Key {TOKEN}',
    'content-type': 'application/json'
}


def generate_map_name() -> str:
    return 'ts_' + str(time())


def create_dataset(data: str) -> str:
    response = requests.post(
        f'{EXTERNAL_API_URL}/datasets',
        data=data,
        headers=HEADERS
    )

    if response.status_code == 201:
        data = response.json()
        return data['id']


def create_map(dataset_id: str) -> str:
    data = {
        'datasets_ids': [dataset_id],
        'name': generate_map_name(),
        'folder_id': None,
        'analyses_results_ids': []
    }
    response = requests.post(
        f'{API_URL}/maps',
        data=json.dumps(data),
        headers=HEADERS
    )

    if response.status_code == 200:
        data = response.json()
        return data['data']['id']


def share_map(map_id: str) -> str:
    response = requests.get(
        f'{API_URL}/maps/share/{map_id}/link',
        headers=HEADERS
    )

    if response.status_code == 200:
        data = response.json()
        shared_map_id = data['data']['id']

        response = requests.patch(
            f'{API_URL}/maps/share/{shared_map_id}',
            data=json.dumps({'shared': True}),
            headers=HEADERS
        )

        return shared_map_id


def get_shared_map_url(shared_map_id: str) -> str:
    return f'{BASE_URL}/app/maps/shared/{shared_map_id}'


with open('example.geojson', 'r') as file:
    data = file.read()

dataset_id = create_dataset(data)
print('Dataset id:', dataset_id)

map_id = create_map(dataset_id)
print('Map id:', dataset_id)

shared_map_id = share_map(map_id)
print('Shared map id:', dataset_id)

shared_map_url = get_shared_map_url(shared_map_id)
print('Shared map URL:', shared_map_url)
