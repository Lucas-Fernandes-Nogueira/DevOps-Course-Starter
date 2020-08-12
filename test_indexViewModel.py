import pytest
from viewModels.indexViewModel import IndexViewModel
from to_do_item import ToDoItem
from to_do_item import Status


def test_items():
    # given
    item1 = ToDoItem(1, "First task", Status.DONE)
    item2 = ToDoItem(2, "Second task", Status.TODO)
    items = [item1, item2]

    # when
    indexViewModel = IndexViewModel(items)

    # then
    assert indexViewModel.items == items

def test_to_do_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO)
    item2 = ToDoItem(2, "Second task", Status.DOING)
    items = [item1, item2]
    to_do_items = [item1]

    # when
    indexViewModel = IndexViewModel(items)

    # then
    assert indexViewModel.to_do_items == to_do_items

def test_doing_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO)
    item2 = ToDoItem(2, "Second task", Status.DOING)
    items = [item1, item2]
    doing_items = [item2]

    # when
    indexViewModel = IndexViewModel(items)

    # then
    assert indexViewModel.doing_items == doing_items

def test_done_items():
    # given
    item1 = ToDoItem(1, "First task", Status.TODO)
    item2 = ToDoItem(2, "Second task", Status.DOING)
    item3 = ToDoItem(3, "Third task", Status.DONE)
    item4 = ToDoItem(4, "Fourth task", Status.DONE)

    items = [item1, item2, item3, item4]
    done_items = [item3, item4]

    # when
    indexViewModel = IndexViewModel(items)

    # then
    assert indexViewModel.done_items == done_items