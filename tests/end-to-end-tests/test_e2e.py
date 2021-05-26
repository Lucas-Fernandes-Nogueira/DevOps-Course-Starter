import app as app
from dotenv import find_dotenv, load_dotenv
import pytest
import requests
import os
from threading import Thread
import mongo_api as mongo
from selenium import webdriver
import flask_login
from user import User
from _pytest.monkeypatch import MonkeyPatch

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    if file_path:
        load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    os.environ["DATABASE"] = "test-todo-app"

    # construct the new application
    application = app.create_app()
    application.config['LOGIN_DISABLED'] = True

    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    mongo_api = mongo.MongoApi(
        os.getenv('MONGO_USERNAME'),
        os.getenv('MONGO_PASSWORD'),
        os.getenv('MONGO_URL'),
        "test-todo-app")
    mongo_api.delete_database("test-todo-app")

def test_task_journey(driver, test_app, monkeypatch):
    # mock the test user
    monkeypatch.setattr(flask_login, "current_user", User('test-user'))

    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    inputBox = driver.find_element_by_id("title")
    submitButton = driver.find_elements_by_xpath("/html/body/div/div[2]/div[1]/ul/form/button")[0]

    inputBox.send_keys("test item")
    submitButton.click()

    toDoItems = driver.find_elements_by_css_selector('.to-do-list li form')

    matching_items = [ item for item in toDoItems if item.text == "test item" ]
    assert len(matching_items) == 1
