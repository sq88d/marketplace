# класс User и Product
from data.users import User
from data.products import Product

# форма регистрации и входа в ЛК
from data.user_forms import RegistrationForm, LoginForm

# форма добавления нового товара
from data.product_forms import ProductForm

# подключение базы данных
from data import db_session

# библиотека flask
from flask import Flask, render_template, redirect, request, abort

# библиотека flask_login
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'I am Giraffe!'


# главная страница
@app.route("/")
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter()

    return render_template("index.html", products=products, title='Интернет-магазин')


# получение данных о пользователе
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# регистрация пользователя
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        if len(form.password.data) >= 8:
            if form.password.data != form.password_again.data:
                return render_template('registration.html', title='Регистрация', form=form,
                                       message="Введенные пароли не совпадают")

            db_sess = db_session.create_session()

            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('registration.html', title='Регистрация', form=form,
                                       message="Введенная электронная почта уже используется")

            user = User()

            user.email = form.email.data
            user.set_password(form.password.data)
            user.name = form.name.data
            db_sess.add(user)
            db_sess.commit()

            return redirect('/')
        else:
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Длина пароля меньше 8 символов")

    return render_template('registration.html', title='Регистрация', form=form, message='')


# вход в личный кабинет
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html', message="Неправильный логин или пароль", form=form)

    return render_template('login.html', title='Авторизация', form=form)


# выход из личного кабинета
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# добавить товар в корзину
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(Product).filter(Product.title == form.title.data).first():
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Введенное название товара уже используется")

        product = Product()
        product.title = form.title.data
        product.content = form.content.data
        product.price = form.price.data

        current_user.products.append(product)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')

    return render_template('create.html', message='', form=form, title="Новый товар")


def main():
    db_session.global_init("db/store.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
