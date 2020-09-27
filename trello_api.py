import requests
import os
from copy import deepcopy
from to_do_item import ToDoItem
from to_do_item import Status

API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')
BOARD_ID = os.getenv('BOARD_ID')

CREDENTIALS = { 'key': API_KEY, 'token': TOKEN }

TRELLO_API_BASE_URL = 'https://api.trello.com/1'

TO_DO_LIST_ID = None
DOING_LIST_ID = None
DONE_LIST_ID = None

def load_to_do_list_id_if_none():
    global TO_DO_LIST_ID
    if TO_DO_LIST_ID is None:
        TO_DO_LIST_ID = get_list_id_by_name("To Do", BOARD_ID)

def load_doing_list_id_if_none():
    global DOING_LIST_ID
    if DOING_LIST_ID is None:
        DOING_LIST_ID = get_list_id_by_name("Doing", BOARD_ID)

def load_done_list_id_if_none():
    global DONE_LIST_ID
    if DONE_LIST_ID is None:
        DONE_LIST_ID = get_list_id_by_name("Done", BOARD_ID)

def load_all_list_ids():
    load_to_do_list_id_if_none()
    load_doing_list_id_if_none()
    load_done_list_id_if_none()

def get_items():
    items = []
    fetch_and_append_to_do_list_items(items)
    fetch_and_append_doing_list_items(items)
    fetch_and_append_done_list_items(items)
    sort_items_by_id(items)
    return items

def get_id(item):
    return item.id

def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)

def add_item(title):
    load_to_do_list_id_if_none()
    params = deepcopy(CREDENTIALS)
    params['name'] = title
    params['idList'] = TO_DO_LIST_ID
    requests.post(f'{TRELLO_API_BASE_URL}/cards', params=params)

def toggle_status(item):
    load_all_list_ids()
    params = deepcopy(CREDENTIALS)
    if (item.status == Status.DONE):
        params['idList'] = TO_DO_LIST_ID
    elif (item.status == Status.DOING):
        params['idList'] = DONE_LIST_ID
    else:
        params['idList'] = DOING_LIST_ID
    
    requests.put(f'{TRELLO_API_BASE_URL}/cards/{item.id}', params=params)

def remove_item(item):
    requests.delete(f'{TRELLO_API_BASE_URL}/cards/{item.id}', params=CREDENTIALS)

def sort_items_by_id(items):
    items.sort(key=get_id)

def fetch_and_append_to_do_list_items(items):
    load_to_do_list_id_if_none()
    r = requests.get(f'{TRELLO_API_BASE_URL}/lists/{TO_DO_LIST_ID}/cards', params=CREDENTIALS)
    for item in r.json():
        items.append(ToDoItem.parse_json_to_do_item(item))

def fetch_and_append_doing_list_items(items):
    load_doing_list_id_if_none()
    r = requests.get(f'{TRELLO_API_BASE_URL}/lists/{DOING_LIST_ID}/cards', params=CREDENTIALS)
    for item in r.json():
        items.append(ToDoItem.parse_json_doing_item(item))

def fetch_and_append_done_list_items(items):
    load_done_list_id_if_none()
    r = requests.get(f'{TRELLO_API_BASE_URL}/lists/{DONE_LIST_ID}/cards', params=CREDENTIALS)
    for item in r.json():
        items.append(ToDoItem.parse_json_done_item(item))

def create_board(board_name):
    params = deepcopy(CREDENTIALS)
    params['name'] = board_name
    response = requests.post(f'{TRELLO_API_BASE_URL}/boards/', params=params)
    return response.id

def delete_board(board_id):
    requests.delete(f'{TRELLO_API_BASE_URL}/boards/{board_id}', params=CREDENTIALS)

def get_lists(board_id):
    r = requests.get(f'{TRELLO_API_BASE_URL}/boards/{board_id}/lists', params=CREDENTIALS)
    lists = []
    for item in r.json():
        lists.append({"id": item["id"], "name": item["name"]})
    return lists

def get_list_id_by_name(list_name, board_id):
    lists = get_lists(board_id)
    board_list = next((item for item in lists if item["name"] == list_name))
    return board_list["id"]

