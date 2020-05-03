from bookstore.bookstore_web import app
from flask import render_template


@app.route('/')
def index():
    user = {'username': 'Błażej'}
    title = 'Księgania LoremIpsum'
    return render_template('index.html', title=title, user=user)
