from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField


# форма добавления нового товара
class ProductForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    content = TextAreaField("Информация о товаре")
    price = TextAreaField("Цена")
    submit = SubmitField('Добавить')
