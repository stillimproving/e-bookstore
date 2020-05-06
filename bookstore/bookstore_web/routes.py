from flask import render_template, flash, redirect, url_for
from bookstore.bookstore_web import app
from bookstore.bookstore_web.forms import LoginForm
from bookstore.db_connectors import db_connector

NAME = 'e-Bookstore'


@app.route('/')
@app.route('/index')
def index():
    books = db_connector.get_books(category='Thriller')[:5]
    return render_template('index.html', global_title=NAME, after_title=" | Home", books=books,
                           book_link='privacy_policy')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.usermail.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', global_title=NAME, after_title=' | Log In', form=form)


@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html', global_title=NAME, after_title=' | Terms of use')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', global_title=NAME, after_title=' | Privacy policy')
