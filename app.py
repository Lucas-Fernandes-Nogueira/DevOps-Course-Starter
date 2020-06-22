from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/')
def index():
    items = session.get_items()
    return render_template('index.html', items=items)

@app.route('/new-item', methods=['POST'])
def addItem():
    title = request.form.get('title') 
    if title:
        session.add_item(title)
    return redirect(url_for('index'))

@app.route('/toggle-status', methods=['POST'])
def toggleStatus():
    itemId = request.form.get('id')
    item = session.get_item(itemId)

    session.toggle_status(item)

    return redirect(url_for('index'))

@app.route('/remove-item', methods=['POST'])
def removeItem():
    itemId = request.form.get('id')
    item = session.get_item(itemId)
    session.remove_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
