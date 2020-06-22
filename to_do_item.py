class ToDoItem:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status

    @staticmethod
    def parse_json_not_started_item(json_item):
        return ToDoItem(json_item['id'], json_item['name'], 'Not Started')

    @staticmethod
    def parse_json_completed_item(json_item):
        return ToDoItem(json_item['id'], json_item['name'], 'Completed')

