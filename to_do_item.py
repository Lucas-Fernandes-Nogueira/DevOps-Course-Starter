from enum import Enum

class ToDoItem:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status

    def isDone(self):
        return self.status == Status.DONE

    def isDoing(self):
        return self.status == Status.DOING

    def isTodo(self):
        return self.status == Status.TODO

    @classmethod
    def parse_json_to_do_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.TODO)

    @classmethod
    def parse_json_doing_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.DOING)

    @classmethod
    def parse_json_done_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], Status.DONE) 


class Status(Enum):
    TODO = 1
    DOING = 2
    DONE = 3