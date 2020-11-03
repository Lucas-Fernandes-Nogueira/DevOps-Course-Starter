from flask import Flask, render_template, request, redirect, url_for
import trello_api as trello
from viewModels.indexViewModel import IndexViewModel
from dotenv import find_dotenv, load_dotenv

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        items = trello.get_items()
        index_view_model = IndexViewModel(items, False)
        return render_template('index.html', viewModel=index_view_model)

    @app.route('/new-item', methods=['POST'])
    def addItem():
        title = request.form.get('title')
        if title:
            trello.add_item(title)
        return redirect(url_for('index'))

    @app.route('/toggle-status', methods=['POST'])
    def toggleStatus():
        item_id = request.form.get('id')
        item = trello.get_item(item_id)

        trello.toggle_status(item)

        return redirect(url_for('index'))

    @app.route('/remove-item', methods=['POST'])
    def removeItem():
        item_id = request.form.get('id')
        item = trello.get_item(item_id)
        trello.remove_item(item)
        return redirect(url_for('index'))
    
    return app

if __name__ == '__main__':
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    create_app().run()
