# класс User и Product
from data.users import User
from data.products import Product

# формы регистрации и входа в ЛК
from data.user_forms import RegisterForm, LoginForm

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


# получение пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# 4. Кроме того, наша модель для пользователей
# должна содержать ряд методов
# для корректной работы flask-login,
# но мы не будем создавать их руками,
# а воспользуемся множественным наследованием.
# см. файл: \data\users.py

# выход из личного кабинета
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# @app.route('/news', methods=['GET', 'POST'])
# @login_required
# def add_news():
#     form = NewsForm()
#     if form.validate_on_submit():  # проверка, авторизовался ли пользователь
#         db_sess = db_session.create_session()
#         news = News()
#         news.title = form.title.data
#         news.content = form.content.data
#         news.is_private = form.is_private.data
#         current_user.news.append(news)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('news.html', title='Добавление новости', form=form)


# @app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#     if news:
#         db_sess.delete(news)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')


# @app.route('/news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = NewsForm()
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#     if request.method == "GET":
#         # db_sess = db_session.create_session()
#         # news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#         if news:
#             form.title.data = news.title
#             form.content.data = news.content
#             form.is_private.data = news.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         # db_sess = db_session.create_session()
#         # news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#         if news:
#             news.title = form.title.data
#             news.content = form.content.data
#             news.is_private = form.is_private.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('news.html', title='Редактирование новости', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
        # проверка на совпадение паролей
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()

        # проверка на существующего пользователя
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


# вход в личный кабинет
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Не забудьте импортировать класс LoginForm и метод login_user из модуля flask-login.
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # поиск пользователя в БД по введенной почте
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        # проверка на правильность пароля
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            return redirect("/")

        # если пароль неверный
        return render_template('login.html', message="Неправильный логин или пароль", form=form)

    # если авторизация не пройдена
    return render_template('login.html', title='Авторизация', form=form)


# @app.route("/")
# def index():
#     db_sess = db_session.create_session()
#     return render_template("index.html")


@app.route("/product/<int:id>")
def product(id):
    db_sess = db_session.create_session()
    title = db_sess.query(Product).filter(Product.id == id)
    print(title)

    return render_template("product.html", title=f'{title}')


def main():
    db_session.global_init("db/accounts.db")
    app.run(port=8080, host='127.0.0.1')

    # names = ['Медведь', 'Брахиозавр', 'Бурый медведь', 'Крокодил', 'Хаски',
    #          'Мышка', 'Панда', 'Пантера', 'Кролик', 'Акула',
    #          'Змея', 'Стегозавр', 'Тосты', 'Трицератопс', 'Тираннозавр']
    #
    # links = ['bear-toy.jpg', 'brachiosaurus-toy.jpg', 'brown-bear-toy.jpg', 'crocodile-toy.jpg', 'husky-toy.jpg',
    #          'mouse-toy.jpg', 'panda-toy.jpg', 'panther-toy.jpg', 'rabbit-toy.jpg', 'shark-toy.jpg',
    #          'snake-toy.jpg', 'stegosaurus-toy.jpg', 'toasts-toy.jpg', 'triceratops-toy.jpg', 'tyrannosaurus-toy.jpg']
    #
    # for i in range(len(links)):
    #     links[i] = f'static\images\ ' + links[i]
    #
    # print(links)


if __name__ == '__main__':
    main()
