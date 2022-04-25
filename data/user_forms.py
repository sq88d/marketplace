from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField


# форма регистрации
class RegistrationForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль (минимум 8 символов)', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


# форма входа в личный кабинет
class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
