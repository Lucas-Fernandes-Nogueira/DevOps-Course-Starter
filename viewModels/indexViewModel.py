from to_do_item import Status
import datetime

class IndexViewModel:
    def __init__(self, items, show_all_done_items, user_has_writer_role):
        self._items = items
        self._show_all_done_items = show_all_done_items
        self._user_has_writer_role = user_has_writer_role

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

    @property
    def show_all_done_items(self):
        return self._show_all_done_items

    @property
    def recent_done_items(self):
        date_today = datetime.datetime.now().date()
        return list(filter(lambda item: item.date_last_activity.date() == date_today, self.done_items))

    @property
    def older_done_items(self):
        date_today = datetime.datetime.now().date()
        return list(filter(lambda item: item.date_last_activity.date() < date_today, self.done_items))
    
    @property
    def user_has_writer_role(self):
        return self._user_has_writer_role
