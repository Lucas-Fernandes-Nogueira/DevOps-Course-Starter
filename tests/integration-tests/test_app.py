import app as app
from dotenv import find_dotenv, load_dotenv
import pytest
from _pytest.monkeypatch import MonkeyPatch
import requests
import mongomock
import pymongo
import flask_login
from user import User

@pytest.fixture
def client(monkeypatch): 
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    mongoClient = mongomock.MongoClient()
    db = mongoClient["todo-app"]
    todo_list = db.todo
    doing_list = db.doing
    done_list = db.done
    todo_list.insert_one({"_id": "5f4807fd48a3760de9da91df", "dateLastActivity": "2020-09-19T19:48:56.175Z", "task": "Task 1"})
    todo_list.insert_one({"_id": "5f54f1d40cfb591e93ddf2ec", "dateLastActivity": "2020-09-18T22:43:29.708Z", "task": "Task 2"})
    doing_list.insert_one({"_id": "5f54c6c9844e7f7512a0ea2d", "dateLastActivity": "2020-09-19T19:48:55.367Z", "task": "Task 3"})
    done_list.insert_one({"_id": "5f54c8717586957307e1b943", "dateLastActivity": "2020-09-06T18:06:53.483Z", "task": "Task 4"})
    
    def mock_mongo_client(*args, **kwards):
        return mongoClient

    monkeypatch.setattr(pymongo, "MongoClient", mock_mongo_client)
    monkeypatch.setattr(flask_login, "current_user", User('test-user'))

    # Create the new app.
    test_app = app.create_app()
    test_app.config['LOGIN_DISABLED'] = True

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(client, monkeypatch):
    # when
    response = client.get('/')

    # then
    assert "Task 1" in str(response.data)
    assert "Task 2" in str(response.data)
    assert "Task 3" in str(response.data)
    assert "Task 4" in str(response.data)