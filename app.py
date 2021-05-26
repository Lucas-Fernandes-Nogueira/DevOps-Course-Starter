from flask import Flask, render_template, request, redirect, url_for
import mongo_api as mongo
from viewModels.indexViewModel import IndexViewModel
from dotenv import find_dotenv, load_dotenv
import os
import flask_login
import requests
import json
from user import User
from functools import wraps

GITHUB_AUTHORIZATION_URI = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URI = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URI = 'https://api.github.com/user'

login_manager = flask_login.LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    return redirect(GITHUB_AUTHORIZATION_URI + '?client_id=' + os.getenv('CLIENT_ID'))

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    login_manager.init_app(app)
    storage = mongo.MongoApi(
        os.getenv('MONGO_USERNAME'),
        os.getenv('MONGO_PASSWORD'),
        os.getenv('MONGO_URL'),
        os.getenv('DATABASE'))

    def user_has_writer_role(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if flask_login.current_user and flask_login.current_user.has_writer_role():
                return function(*args, **kwargs)
            else:
                return redirect(url_for('index'))
        return decorated_function

    @app.route('/login/callback')
    def login_callback():
        access_token = requests.post(GITHUB_TOKEN_URI, 
            data = {
            'client_id':  os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'code': request.args.get('code')
            },
            headers = {
                "Accept": "application/json",
            })
        token = 'token ' + json.loads(access_token.text)['access_token']
        user_info = requests.get(GITHUB_USER_URI, headers = {'Authorization': token})
        user_id = json.loads(user_info.text)['id']
        flask_login.login_user(User(user_id))
        return redirect(url_for('index'))

    @app.route('/')
    @flask_login.login_required
    def index():
        items = storage.get_items()
        index_view_model = IndexViewModel(items, False, flask_login.current_user.has_writer_role())
        return render_template('index.html', viewModel=index_view_model)

    @app.route('/new-item', methods=['POST'])
    @user_has_writer_role
    @flask_login.login_required
    def addItem():
        title = request.form.get('title')
        if title:
            storage.add_item(title)
        return redirect(url_for('index'))
    
    @app.route('/toggle-status', methods=['POST'])
    @user_has_writer_role
    @flask_login.login_required
    def toggleStatus():
        item_id = request.form.get('id')
        item = storage.get_item(item_id)
        storage.toggle_status(item)

        return redirect(url_for('index'))

    
    @app.route('/remove-item', methods=['POST'])
    @user_has_writer_role
    @flask_login.login_required
    def removeItem():
        item_id = request.form.get('id')
        item = storage.get_item(item_id)
        storage.remove_item(item)
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    create_app().run()
