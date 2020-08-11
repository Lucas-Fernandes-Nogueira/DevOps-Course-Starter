from flask import Flask, render_template, request, redirect, url_for
import trello_api as trello
from viewModels.indexViewModel import IndexViewModel

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/')
def index():
    items = trello.get_items()
    indexViewModel = IndexViewModel(items)
    return render_template('index.html', viewModel=indexViewModel)

@app.route('/new-item', methods=['POST'])
def addItem():
    title = request.form.get('title') 
    if title:
        trello.add_item(title)
    return redirect(url_for('index'))

@app.route('/toggle-status', methods=['POST'])
def toggleStatus():
    itemId = request.form.get('id')
    item = trello.get_item(itemId)

    trello.toggle_status(item)

    return redirect(url_for('index'))

@app.route('/remove-item', methods=['POST'])
def removeItem():
    itemId = request.form.get('id')
    item = trello.get_item(itemId)
    trello.remove_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
