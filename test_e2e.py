import app as app
from dotenv import find_dotenv, load_dotenv
import pytest
from _pytest.monkeypatch import MonkeyPatch
import requests
from mock_trello_get_response import mock_trello_response
import os
from threading import Thread
import trello_api
from selenium import webdriver


@pytest.fixture(scope="module")
def driver():
 with webdriver.Firefox() as driver:
     yield driver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    board_id = trello_api.create_board("Test Board")
    os.environ['BOARD_ID'] = board_id 

    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    trello_api.delete_board(board_id)

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    inputBox = driver.find_element_by_id("title")
    submitButton = driver.find_elements_by_xpath("/html/body/div/div[2]/div[1]/ul/form/button")[0]

    inputBox.send_keys("test item")
    submitButton.click()

    toDoItems = driver.find_elements_by_css_selector('.to-do-list li form')

    counter = 0

    for item in toDoItems:
        if item.text == "test item":
            counter += 1
    
    assert counter == 1
