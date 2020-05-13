from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, Form
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    usermail = StringField(
        label='Email address',
        validators=[DataRequired(message='required')],
        render_kw={'placeholder': 'Email address'})
    password = PasswordField(
        label='Password',
        validators=[DataRequired(message='required')],
        render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    name = StringField(
        label='First name',
        validators=[DataRequired(message='required')],
        render_kw={'placeholder': 'First name'})
    surname = StringField(
        label='Last name',
        validators=[DataRequired(message='required')],
        render_kw={'placeholder': 'Last name'})
    email = StringField(
        label='Email address',
        validators=[DataRequired(message='required'), Email('not an email')],
        render_kw={'placeholder': 'Email address'})
    password = PasswordField(
        label='Password', validators=[DataRequired(message='required')],
        render_kw={'placeholder': 'Password'})
    confirm = PasswordField(
        label='Confirm password', validators=[DataRequired(message='required'), EqualTo('password', message='no match')],
        render_kw={'placeholder': 'Confirm password'})
    phone = StringField(
        label='Phone',
        render_kw={'placeholder': 'Phone'})
    street = StringField(
        label='Street',
        render_kw={'placeholder': 'Street'})
    postal_code = StringField(
        label='Postal code',
        render_kw={'placeholder': 'Postal code'})
    city = StringField(
        label='City',
        render_kw={'placeholder': 'City'})
    country = StringField(
        label='Country',
        render_kw={'placeholder': 'Country'})
    accept = BooleanField(label='I accept ', validators=[DataRequired(message='required')])
    submit = SubmitField(label='Sign In')


class SearchForm(Form):
    search_input = StringField('Search', render_kw={'type': 'search', 'placeholder': 'Search for books...'})
    choices = [
        ('Title', 'Title'),
        ('Author', 'Author'),
        ('Category', 'Category'),
        ('Publisher', 'Publisher'),
        ('ISBN', 'ISBN')]
    type = SelectField('Search type', choices=choices)
    submit = SubmitField('🔍')


class EditUserForm(FlaskForm):
    name = StringField('First name', validators=[DataRequired()], render_kw={'id': 'edit'})
    surname = StringField('Last name', validators=[DataRequired()], render_kw={'id': 'edit'})
    phone = StringField('Phone', render_kw={'id': 'edit'})
    street = StringField('Street', render_kw={'id': 'edit'})
    postal_code = StringField('Postal code', render_kw={'id': 'edit'})
    city = StringField('City', render_kw={'id': 'edit'})
    country = StringField('Country', render_kw={'id': 'edit'})
    submit = SubmitField('Submit', render_kw={'id': 'edit'})


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        label='Old password',
        validators=[DataRequired(message='required')],
        render_kw={'id': 'pass', 'placeholder': 'Old password'})
    new_password = PasswordField(
        label='New password',
        validators=[DataRequired(message='required')],
        render_kw={'id': 'pass', 'placeholder': 'New password'})
    confirm = PasswordField(
        label='Confirm password',
        validators=[DataRequired(message='required'), EqualTo('new_password', message='no match')],
        render_kw={'id': 'pass', 'placeholder': 'Confirm password'})
    change = SubmitField('Change')


class DeleteUserForm(FlaskForm):
    delete = SubmitField('Delete me!')
