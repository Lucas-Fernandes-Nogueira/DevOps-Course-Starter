import app as app
from dotenv import find_dotenv, load_dotenv
import pytest
from _pytest.monkeypatch import MonkeyPatch
import requests
from mock_trello_get_response import mock_trello_response

@pytest.fixture
def client(monkeypatch):
    def mock_get_requests(*args, **kwards):
        return MockListsResponse()
    monkeypatch.setattr(requests, 'get', mock_get_requests)
    
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class MockCardsResponse:
    @staticmethod
    def json():
        return mock_trello_response

class MockListsResponse:
    @staticmethod
    def json():
        return [{"id": 1, "name": "To Do"}, {"id": 2, "name": "Doing"}, {"id": 3, "name": "Done"}]

def test_index_page(client, monkeypatch):
    # given
    def mock_get_requests(*args, **kwargs):
        if "cards" in args[0]:
            return MockCardsResponse()
        elif "lists" in args[0]:
            return MockListsResponse()

    monkeypatch.setattr(requests, 'get', mock_get_requests)

    # when
    response = client.get('/')

    # then
    assert "Task 1" in str(response.data)
    assert "Task 2" in str(response.data)
    assert "Task 3" in str(response.data)
    assert "Task 4" in str(response.data)