from to_do_item import Status

class IndexViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return list(filter(lambda item: item.status == Status.TODO, self._items))

    @property
    def doing_items(self):
        return list(filter(lambda item: item.status == Status.DOING, self._items))

    @property
    def done_items(self):
        return list(filter(lambda item: item.status == Status.DONE, self._items))