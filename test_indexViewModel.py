import pytest
from viewModels.indexViewModel import IndexViewModel
from to_do_item import ToDoItem
from to_do_item import Status
import datetime
from _pytest.monkeypatch import MonkeyPatch
from freezegun import freeze_time

FAKE_TIME = datetime.datetime.combine(datetime.date(2020, 9, 20), datetime.time(1,0))

def test_items():
    # given
    item1 = ToDoItem(1, "First task", Status.DONE, datetime.date(2020, 5, 22))
    item2 = ToDoItem(2, "Second task", Status.TODO, datetime.date(2020, 5, 22))
    items = [item1, item2]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.items == items

def test_to_do_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO, datetime.date(2020, 5, 22))
    item2 = ToDoItem(2, "Second task", Status.DOING, datetime.date(2020, 5, 22))
    items = [item1, item2]
    to_do_items = [item1]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.to_do_items == to_do_items

def test_doing_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO, datetime.date(2020, 5, 22))
    item2 = ToDoItem(2, "Second task", Status.DOING, datetime.date(2020, 5, 22))
    items = [item1, item2]
    doing_items = [item2]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.doing_items == doing_items

def test_done_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO, datetime.date(2020, 5, 22))
    item2 = ToDoItem(2, "Second task", Status.DOING, datetime.date(2020, 5, 22))
    item3 = ToDoItem(3, "Third task", Status.DONE, datetime.date(2020, 5, 22))
    item4 = ToDoItem(4, "Fourth task", Status.DONE, datetime.date(2020, 5, 22))

    items = [item1, item2, item3, item4]
    done_items = [item3, item4]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.done_items == done_items

def test_show_all_done_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO, datetime.date(2020, 5, 22))
    item2 = ToDoItem(2, "Second task", Status.DOING, datetime.date(2020, 5, 22))
    item3 = ToDoItem(3, "Third task", Status.DONE, datetime.date(2020, 5, 22))

    items = [item1, item2, item3]
    
    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.show_all_done_items == False

@freeze_time("Sep 20th, 2020")
def test_recent_done_items():
    # given

    item1 = ToDoItem(1, "First task", Status.TODO, datetime.datetime.combine(datetime.date(2020, 5, 22), datetime.time(1,0)))
    item2 = ToDoItem(2, "Second task", Status.DONE, datetime.datetime.combine(datetime.date(2020, 8, 26), datetime.time(1,0)))
    item3 = ToDoItem(3, "Third task", Status.DONE, datetime.datetime.combine(datetime.date(2020, 9, 20), datetime.time(1,0)))

    items = [item1, item2, item3]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.recent_done_items == [item3]

@freeze_time("Sep 20th, 2020")
def test_older_done_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO, datetime.datetime.combine(datetime.date(2020, 5, 22), datetime.time(1,0)))
    item2 = ToDoItem(2, "Second task", Status.DONE, datetime.datetime.combine(datetime.date(2020, 8, 26), datetime.time(1,0)))
    item3 = ToDoItem(3, "Third task", Status.DONE, datetime.datetime.combine(datetime.date(2020, 9, 20), datetime.time(1,0)))

    items = [item1, item2, item3]

    # when
    indexViewModel = IndexViewModel(items, False)

    # then
    assert indexViewModel.older_done_items == [item2]
