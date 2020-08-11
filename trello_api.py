import requests
import os
from copy import deepcopy
from to_do_item import ToDoItem

API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')
BOARD_ID = os.getenv('BOARD_ID')
TO_DO_LIST_ID = os.getenv('TO_DO_LIST_ID')
DONE_LIST_ID = os.getenv('DONE_LIST_ID')

CREDENTIALS = { 'key': API_KEY, 'token': TOKEN }

TRELLO_API_BASE_URL = 'https://api.trello.com/1'

def get_items():
    items = []
    fetch_and_append_to_do_list_items(items)
    fetch_and_append_done_list_items(items)
    sort_items_by_id(items)
    return items

def get_id(item):
    return item.id

def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title):
    params = deepcopy(CREDENTIALS)
    params['name'] = title
    params['idList'] = TO_DO_LIST_ID
    requests.post(f'{TRELLO_API_BASE_URL}/cards', params=params)

def toggle_status(item):
    params = deepcopy(CREDENTIALS)
    if (item.status == 'Completed'):
        params['idList'] = TO_DO_LIST_ID
    else:
        params['idList'] = DONE_LIST_ID
    
    requests.put(f'{TRELLO_API_BASE_URL}/cards/{item.id}', params=params)

def remove_item(item):
    requests.delete(f'{TRELLO_API_BASE_URL}/cards/{item.id}', params=CREDENTIALS)

def sort_items_by_id(items):
    items.sort(key=get_id)

def fetch_and_append_to_do_list_items(items):
    r = requests.get(f'{TRELLO_API_BASE_URL}/lists/{TO_DO_LIST_ID}/cards', params=CREDENTIALS)
    for item in r.json():
        items.append(ToDoItem.parse_json_not_started_item(item))

def fetch_and_append_done_list_items(items):
    r = requests.get(f'{TRELLO_API_BASE_URL}/lists/{DONE_LIST_ID}/cards', params=CREDENTIALS)
    for item in r.json():
        items.append(ToDoItem.parse_json_completed_item(item))