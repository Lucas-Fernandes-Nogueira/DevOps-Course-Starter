import pytest
from viewModels.indexViewModel import IndexViewModel
from to_do_item import ToDoItem
from to_do_item import Status


def test_items():
    item1 = ToDoItem(1, "First task", Status.DONE)
    item2 = ToDoItem(2, "Second task", Status.TODO)

    items = [item1, item2]

    indexViewModel = IndexViewModel(items)

    assert indexViewModel.items == items

#def test_to_do_items():
#    item1 = ToDoItem(1, "First task", Status.TODO)
#    item2 = ToDoItem(2, "Second task", Status.DOING)
#
#    items = [item1, item2]
#
#    to_do_items = [item1]
#
#    indexViewModel = IndexViewModel(items)
#
#    assert indexViewModel.to_do_items == to_do_items