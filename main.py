from flask import Flask, render_template, redirect, request, make_response, session, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user  # , current_user
from werkzeug.exceptions import abort

import data
from data import db_session
from data.AuthorForm import AuthorForm
from data.BookForm import BookForm
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.authors import Authors
from data.books import Books
from data.genres import Genres
from data.users import Users

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# главная страница
@app.route("/")
def index():
    session = db_session.create_session()
    # q- строка с поисковым запросом
    q = request.args.get('q')
    # возвращаем посты
    if q:
        genres = session.query(Genres).filter(Genres.name.contains(q)).order_by(Genres.name.asc())
        authors = session.query(Authors).filter(
            (Authors.name.contains(q)) | (Authors.surname.contains(q)) | (Authors.middlename.contains(q))).order_by(
            Authors.name.asc(), Authors.middlename.asc(), Authors.surname.asc())
        books = session.query(Books).filter(Books.title.contains(q)).order_by(Books.title.asc())
    else:
        genres = session.query(Genres).order_by(Genres.name.asc())
        authors = session.query(Authors).order_by(Authors.name.asc(), Authors.middlename.asc(), Authors.surname.asc())
        books = session.query(Books).order_by(Books.title.asc())

    return render_template("index.html", genres=genres, authors=authors, books=books)


# регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session1 = db_session.create_session()
        if session1.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Users(
            name=form.name.data,
            email=form.email.data,

        )
        user.set_password(form.password.data)
        session1.add(user)
        session1.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(Users).get(user_id)


# логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# список новинок
@app.route('/new')
def new_book():
    session = db_session.create_session()
    books = session.query(Books).order_by(Books.created_date.desc())[:5]
    return render_template("new_book.html", books=books)


# список жанров
@app.route('/genre')
def genre():
    session = db_session.create_session()
    # q- строка с поисковым запросом
    q = request.args.get('q')
    # возвращаем посты
    if q:
        genres = session.query(Genres).filter(Genres.name.contains(q)).order_by(Genres.name.asc())
    else:
        genres = session.query(Genres).order_by(Genres.name.asc())
    return render_template("genres.html", genres=genres)


# список книг определенного жанра по его id
@app.route('/genre/<int:id>')
def genre_detail(id):
    session = db_session.create_session()
    genre = session.query(Genres).filter(Genres.id == id).first()
    print(genre)
    books = genre.books
    return render_template('genre_detail.html', books=books, genre=genre)


# Список авторов
@app.route('/author')
def author():
    session = db_session.create_session()
    # q- строка с поисковым запросом
    q = request.args.get('q')
    # возвращаем посты
    if q:
        authors = session.query(Authors).filter(
            (Authors.name.contains(q)) | (Authors.surname.contains(q)) | (Authors.middlename.contains(q))).order_by(
            Authors.name.asc(), Authors.middlename.asc(), Authors.surname.asc())
    else:
        authors = session.query(Authors).order_by(Authors.name.asc(), Authors.middlename.asc(), Authors.surname.asc())
    return render_template("authors.html", authors=authors)


# список книг автора по его id
@app.route('/author/<int:id>')
def author_detail(id):
    session = db_session.create_session()
    author = session.query(Authors).filter(Authors.id == id).first()
    books = author.books
    return render_template('author_detail.html', books=books, author=author)


@app.route('/author_edit', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        author = Authors()
        author.surname = form.surname.data
        author.name = form.name.data
        author.middlename = form.middlename.data
        session.add(author)
        session.commit()
        return redirect('/')
    return render_template('author_edit.html', title='Добавление новости',
                           form=form)


# информация о книге по ее id
@app.route('/book/<int:id>')
def book(id):
    session = db_session.create_session()
    book = session.query(Books).filter(Books.id == id).first()
    return render_template("book.html", book=book)


# Добавить книгу
@app.route('/book_edit', methods=['GET', 'POST'])
@login_required
def add_book():
    session = db_session.create_session()
    form = BookForm()
    form.genres.choices = [(x.id, x.name) for x in session.query(Genres).all()]
    form.fio.choices = [(x.id, x.name + ' ' + x.middlename + ' ' + x.surname) for x in
                        session.query(Authors).order_by(Authors.name.asc(), Authors.middlename.asc(),
                                                        Authors.surname.asc())]
    if form.validate_on_submit():

        book = Books()
        book.title = form.title.data
        book.description = form.description.data
        book.author_id = form.fio.data
        current_user.books.append(book)
        session.merge(current_user)
        session.commit()

        book1 = session.query(Books).filter(Books.title == form.title.data, Books.author_id == form.fio.data).first()
        # print(book1.author)
        for item in form.genres.data:
            gen = session.query(Genres).filter(Genres.id == item).first()
            book1.genre.append(gen)
        session.commit()

        return redirect('/')
    return render_template('book_edit.html', title='Добавление книги',
                           form=form)


@app.route('/book_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    session = db_session.create_session()
    form = BookForm()
    form.genres.choices = [(x.id, x.name) for x in session.query(Genres).all()]
    form.fio.choices = [(x.id, x.name + ' ' + x.middlename + ' ' + x.surname) for x in
                        session.query(Authors).order_by(Authors.name.asc(), Authors.middlename.asc(),
                                                        Authors.surname.asc())]
    if request.method == "GET":

        book = session.query(Books).filter(Books.id == id, Books.user == current_user).first()
        if book:
            form.title.data = book.title
            form.fio.data = book.author_id
            form.description.data = book.description
            form.genres.data = [genre.id for genre in book.genre]
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        book = session.query(Books).filter(Books.id == id, Books.user == current_user).first()
        if book:
            for genre in book.genre:
                book.genre.remove(genre)
            book.title = form.title.data
            book.description = form.description.data
            book.author_id = form.fio.data
            for item in form.genres.data:
                gen = session.query(Genres).filter(Genres.id == item).first()
                book.genre.append(gen)

            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('book_edit.html', title='Редактирование книги', form=form)


@app.route('/book_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def book_delete(id):
    session = db_session.create_session()
    book = session.query(Books).filter(Books.id == id,
                                       Books.user == current_user).first()
    if book:
        session.delete(book)
        session.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/bookshelf.sqlite")
    app.run(port=8000, debug=True)

    # book.title = "Родосский треугольник"
    # book.description = '''Интересная повесть о запутанном деле,которое расследует знаменитый сыщик Эркюль Пуаро и его помощник.'''
    # book.is_private = 0
    # book.author_id = 3
    # book.user_id = 2
    # session = db_session.create_session()
    # session.add(book)
    # session.commit()
    # book = session.query(Books).filter(Books.id == 8).first()
    # print(book.author)
    # genre = session.query(Genres).filter(Genres.id < 3).all()
    # for gn in genre:
    #     print(gn)
    #     book.genre.append(gn)
    # session.commit()

    # for book in session.query(Books).all():
    #     print(book.author)
    #     print(book.genre)


if __name__ == '__main__':
    main()
