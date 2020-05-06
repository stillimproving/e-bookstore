from flask import render_template, flash, redirect, url_for, request
from bookstore.bookstore_web import app
from bookstore.bookstore_web.forms import LoginForm, SearchForm
from bookstore.db_connectors import db
from bookstore.db_connectors.abstract_connector import BookSearchCategory
from flask_login import current_user, login_user, logout_user

NAME = 'e-Bookstore'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    discount=25
    books = db.search_books(category=BookSearchCategory.DISCOUNT, search_text=discount, operator='>=')[:5]
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', global_title=NAME, after_title=" | Home", books=books, search=search, discount=discount)

@app.route('/results')
def search_results(search):
    search_string = search.data['search_input']
    search_type = search.data['type']
    if search_string == '':
        flash('Empty string is not allowed!')
        return redirect(url_for('index'))
    enum_map = {
        'Title': BookSearchCategory.TITLE,
        'Author': BookSearchCategory.AUTHOR,
        'Category': BookSearchCategory.CATEGORY,
        'Publisher': BookSearchCategory.PUBLISHER,
        'ISBN': BookSearchCategory.ISBN}

    results = db.search_books(category=enum_map[search_type], search_text=search_string)
    if not results:
        flash('No results found for ' + search_type + ': "' + search_string + '"!')
        return redirect('/')
    return render_template('results.html', global_title=NAME, after_title=" | Search results", search=search, results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(form.usermail.data, form.remember_me.data))
        user = db.get_user(form.usermail.data)
        if not user or not user.check_passwd(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', global_title=NAME, after_title=' | Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html', global_title=NAME, after_title=' | Terms of use')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', global_title=NAME, after_title=' | Privacy policy')
