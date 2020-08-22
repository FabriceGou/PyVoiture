from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    """User Login Form."""

    email = StringField('Email', [DataRequired(),
                                  Email('Please enter a valid email address.')])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Log In')