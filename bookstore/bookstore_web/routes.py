from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.datastructures import MultiDict

from bookstore.bookstore_web import app
from bookstore.bookstore_web.forms import LoginForm, SignupForm, SearchForm, EditUserForm, \
    ChangePasswordForm, DeleteUserForm
from bookstore.db_connectors import db
from bookstore.db_connectors.abstract_connector import BookSearchCategory
from bookstore.models import User, Cart

NAME = 'E-BOOKSTORE'
CURRENCY = 'PLN'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    discount=25
    books = db.search_books(category=BookSearchCategory.DISCOUNT, search_text=discount, operator='>=')[:5]
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', global_title=NAME, position='../', after_title=" | Home", currency=CURRENCY, books=books, search=search, discount=discount)


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
    return render_template('results.html', global_title=NAME, position='../', after_title=" | Search results", search=search, results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm(prefix='log')
    if login_form.submit.data and login_form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(form.usermail.data, form.remember_me.data))
        user = db.get_user(login_form.usermail.data)
        if not user or not user.check_passwd(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('index'))
    signup_form = SignupForm(prefix='sign')
    if signup_form.submit.data and signup_form.validate_on_submit():
        if db.get_user(signup_form.email.data):
            flash('Given e-mail already registered')
            return redirect(url_for('login'))

        new_user = User(
            name=signup_form.name.data,
            surname=signup_form.surname.data,
            password = signup_form.password.data,
            street = signup_form.street.data,
            email = signup_form.email.data,
            phone = signup_form.phone.data,
            postal_code = signup_form.postal_code.data,
            city = signup_form.city.data,
            country = signup_form.country.data
        )
        success=db.add_user(new_user)
        if success:
            flash('You are registered, plaease Log in!')
        else:
            flash('Something gone wrong, try again')
        return redirect(url_for('login'))
    return render_template('login.html', global_title=NAME, position='../', after_title=' | Log In', login_form=login_form, signup_form=signup_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user')
@login_required
def user():
    return render_template('user.html', global_title=NAME, position='../', after_title=' | Profile')


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    if request.method=='GET':
        edit_user_form=EditUserForm(
            formdata=MultiDict({
            'name': current_user.name,
            'surname': current_user.surname,
            'phone': current_user.phone,
            'street': current_user.street,
            'postal_code': current_user.postal_code,
            'city': current_user.city,
            'country': current_user.country
        })
        )
    else:
        edit_user_form=EditUserForm()
    if edit_user_form.validate_on_submit():
        updated_user = User(
            user_id=current_user.user_id,
            email=current_user.email,
            password=current_user.password,
            name=edit_user_form.name.data,
            surname=edit_user_form.surname.data,
            street=edit_user_form.street.data,
            phone=edit_user_form.phone.data,
            postal_code=edit_user_form.postal_code.data,
            city=edit_user_form.city.data,
            country=edit_user_form.country.data
        )
        success = db.update_user(updated_user)
        if success:
            flash('Your data has been successfully edited!')
            return redirect(url_for('user'))
        else:
            flash('Something gone wrong, try again')
            return redirect(url_for('edit_user'))
    return render_template('edit_user.html', global_title=NAME, position='../', after_title=' | Edit profile', edit_user_form=edit_user_form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_pass_form=ChangePasswordForm()
    if change_pass_form.validate_on_submit():
        if change_pass_form.old_password.data==current_user.password:
            new_pass_user = User(
                user_id=current_user.user_id,
                email=current_user.email,
                password=change_pass_form.new_password.data,
                name=current_user.name,
                surname=current_user.surname,
                street=current_user.street,
                phone=current_user.phone,
                postal_code=current_user.postal_code,
                city=current_user.city,
                country=current_user.country
            )
            success = db.update_user(new_pass_user)
            if success:
                flash('Your password has been successfully changed!')
                return redirect(url_for('user'))
            else:
                flash('Something gone wrong, try again')
                return redirect(url_for('change_password'))
        else:
            flash('Invalid old password')
            return redirect(url_for('change_password'))
    return render_template('change_password.html', global_title=NAME, position='../', after_title=' | Change password', change_pass_form=change_pass_form)


@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    delete_form = DeleteUserForm()
    if delete_form.is_submitted():
        del_user = current_user
        success = db.delete_user(del_user)
        if success:
            flash('Goodbye! :(')
            return redirect(url_for('logout'))
        else:
            flash('Something gone wrong, try again')
            return redirect(url_for('delete_user'))
    return render_template('delete_user.html', global_title=NAME, position='../', after_title=' | Delete account', delete_form=delete_form)


@app.route('/item/<book_id>', methods=['GET', 'POST'])
def item(book_id):
    book = db.search_books(category=BookSearchCategory.ID, search_text=book_id)[0]
    return render_template('item.html', global_title=NAME, position='../../', after_title=" | "+ book.title, currency=CURRENCY, book=book) #, add_to_cart_form=add_to_cart_form


@app.route('/add_to_cart/<book_id>', methods=['GET'])
def add_to_cart(book_id):
    print ("Add to cart: "+book_id)
    Cart.add_to_cart(current_user.user_id, book_id, 1)
    return ("nothing")


@app.route('/cart')
@login_required
def cart():
    ids_cart = Cart.get_user_cart(current_user.user_id)
    user_cart = dict()
    if ids_cart:
        for book_id, quantity in ids_cart.items():
            user_cart[db.search_books(category=BookSearchCategory.ID, search_text=book_id)[0]] = quantity
    return render_template('cart.html', global_title=NAME, position='../', after_title=" | Cart", currency=CURRENCY, user_cart=user_cart)


@app.route('/order')
@login_required
def order():
    missing_fields=[]
    if not current_user.phone:
        missing_fields.append('Phone')
    if not current_user.street:
        missing_fields.append('Street')
    if not current_user.postal_code:
        missing_fields.append('Postal code')
    if not current_user.city:
        missing_fields.append('City')
    if not current_user.country:
        missing_fields.append('Country')
    return render_template('order.html', global_title=NAME, position='../', after_title=" | Cart", currency=CURRENCY, missing_fields=missing_fields)


@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html', global_title=NAME, position='../', after_title=' | Terms of use')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', global_title=NAME, position='../', after_title=' | Privacy policy')
