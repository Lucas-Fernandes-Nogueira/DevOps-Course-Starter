class ToDoItem:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def parse_json_not_started_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], 'Not Started')

    @classmethod
    def parse_json_completed_item(cls, json_item):
        return cls(json_item['id'], json_item['name'], 'Completed')

