from enum import Enum
from datetime import datetime

class ToDoItem:
    def __init__(self, id, title, status, date_last_activity):
        self.id = id
        self.title = title
        self.status = status
        self.date_last_activity = date_last_activity        

    def isDone(self):
        return self.status == Status.DONE

    def isDoing(self):
        return self.status == Status.DOING

    def isTodo(self):
        return self.status == Status.TODO

    @classmethod
    def parse_json_to_do_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.TODO, cls.parse_date_from_json_item(json_item))

    @classmethod
    def parse_json_doing_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.DOING, cls.parse_date_from_json_item(json_item))

    @classmethod
    def parse_json_done_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.DONE, cls.parse_date_from_json_item(json_item)) 

    @classmethod
    def parse_date_from_json_item(cls, json_item):
        return datetime.strptime(json_item['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ')

class Status(Enum):
    TODO = 1
    DOING = 2
    DONE = 3