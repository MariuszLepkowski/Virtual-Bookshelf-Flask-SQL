from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Books))
    all_books = result.scalars().all()
    is_empty = not bool(all_books)
    return render_template('index.html', all_books=all_books, is_empty=is_empty)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        title = data['title']
        author = data['author']
        rating = data['rating']

        new_book = Books(title=title, author=author, rating=rating)

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit_rating(book_id):
    book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()

    if request.method == 'POST':
        data = request.form
        new_rating = data['new_rating']
        book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book)


@app.route("/delete/<int:book_id>", methods=['GET'])
def delete_book(book_id):
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

