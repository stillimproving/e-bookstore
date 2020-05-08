from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, Form
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    usermail = StringField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In', render_kw={'id': 'login_submit'})


class SignupForm(FlaskForm):
    name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email('Not an email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm password', validators=[
        DataRequired(), EqualTo('password', message='Confirmation password doesn\'t match Password')])
    phone = StringField('Phone')
    street = StringField('Street')
    postal_code = StringField('Postal code')
    city = StringField('City')
    country = StringField('Country')
    submit = SubmitField('Sign In', render_kw={'id': 'signup_submit'})


class SearchForm(Form):
    search_input = StringField('Search')
    choices = [
        ('Title', 'Title'),
        ('Author', 'Author'),
        ('Category', 'Category'),
        ('Publisher', 'Publisher'),
        ('ISBN', 'ISBN')]
    type = SelectField('Search type', choices=choices)
    submit = SubmitField('🔍')
