from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class RegisterForm(FlaskForm):

    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    email = EmailField('email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])