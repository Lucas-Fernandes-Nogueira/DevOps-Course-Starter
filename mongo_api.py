import requests
import os
from copy import deepcopy
from to_do_item import ToDoItem
from to_do_item import Status
from dotenv import find_dotenv, load_dotenv
import pymongo
import datetime
from bson.objectid import ObjectId

class MongoApi:
    def __init__(self, database_username, database_password, database_host, database_name):
        self._client = pymongo.MongoClient(f'mongodb://{database_username}:{database_password}@{database_host}:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@{database_username}@')
        self._database_name = database_name

    @property
    def db(self):
        return self._client[self._database_name]

    @property
    def todo_list(self):
        return self.db.todo

    @property
    def doing_list(self):
        return self.db.doing

    @property
    def done_list(self):
        return self.db.done

    def get_items(self):
        items = []
        self.fetch_and_append_to_do_list_items(items)
        self.fetch_and_append_doing_list_items(items)
        self.fetch_and_append_done_list_items(items)
        self.sort_items_by_id(items)
        return items


    def get_id(self, item):
        return item.id


    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item.id == id), None)


    def add_item(self, title):
        item = {"task": title, "dateLastActivity": self.get_time_string_now()}
        self.todo_list.insert_one(item)


    def toggle_status(self, item):
        if (item.status == Status.DONE):
            self.done_list.delete_one({"_id": ObjectId(item.id)})
            self.todo_list.insert_one({"task": item.title, "dateLastActivity": self.get_time_string_now()})
        elif (item.status == Status.DOING):
            self.doing_list.delete_one({"_id": ObjectId(item.id)})
            self.done_list.insert_one({"task": item.title, "dateLastActivity": self.get_time_string_now()})
        else:
            self.todo_list.delete_one({"_id": ObjectId(item.id)})
            self.doing_list.insert_one({"task": item.title, "dateLastActivity": self.get_time_string_now()})


    def remove_item(self, item):
        if (item.status == Status.DONE):
            self.done_list.delete_one({"_id": ObjectId(item.id)})
        elif (item.status == Status.DOING):
            self.doing_list.delete_one({"_id": ObjectId(item.id)})
        else:
            self.todo_list.delete_one({"_id": ObjectId(item.id)})


    def sort_items_by_id(self, items):
        items.sort(key=self.get_id)


    def fetch_and_append_to_do_list_items(self, items):
        r = self.todo_list.find()
        for item in r:
            items.append(ToDoItem.parse_json_to_do_item(item))


    def fetch_and_append_doing_list_items(self, items):
        r = self.doing_list.find()
        for item in r:
            items.append(ToDoItem.parse_json_doing_item(item))


    def fetch_and_append_done_list_items(self, items):
        r = self.done_list.find()
        for item in r:
            items.append(ToDoItem.parse_json_done_item(item))


    def delete_database(self, database_name):
        self._client.drop_database(database_name)


    def get_lists(self):
        return self.db.list_collection_names()


    def get_time_string_now(self):
        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
