from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Login:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Sig In")


class RegisterForm(FlaskForm):
    username = StringField("Login:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Register")
