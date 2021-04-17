from flask import Flask, render_template, request, redirect, url_for
import mongo_api as mongo
from viewModels.indexViewModel import IndexViewModel
from dotenv import find_dotenv, load_dotenv
import os

def create_app():
    app = Flask(__name__)
    storage = mongo.MongoApi(
        os.getenv('MONGO_USERNAME'),
        os.getenv('MONGO_PASSWORD'),
        os.getenv('MONGO_URL'),
        os.getenv('DATABASE'))

    @app.route('/')
    def index():
        items = storage.get_items()
        index_view_model = IndexViewModel(items, False)
        return render_template('index.html', viewModel=index_view_model)

    @app.route('/new-item', methods=['POST'])
    def addItem():
        title = request.form.get('title')
        if title:
            storage.add_item(title)
        return redirect(url_for('index'))

    @app.route('/toggle-status', methods=['POST'])
    def toggleStatus():
        item_id = request.form.get('id')
        item = storage.get_item(item_id)
        storage.toggle_status(item)

        return redirect(url_for('index'))

    @app.route('/remove-item', methods=['POST'])
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
