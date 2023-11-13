from flask import Blueprint, request, jsonify
from app import db
from app.models import Book

books_blueprint = Blueprint('books', __name__)

@books_blueprint.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    publication_year = data.get('publication_year')

    if not title or not author or not genre or not publication_year:
        return jsonify({'message': 'Missing required fields'}), 400

    book = Book(title=data['title'], author=data['author'], genre=data['genre'], publication_year=data['publication_year'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@books_blueprint.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'title': book.title, 'author': book.author, 'genre': book.genre, 'publication_year': book.publication_year} for book in books])


@books_blueprint.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    filter_genre = request.args.get('genre')
    filter_year = request.args.get('year')
    min_rating = request.args.get('min_rating')

    query_filter = Book.query
    if query:
        query_filter = query_filter.filter(
            (Book.title.ilike(f'%{query}%')) | 
            (Book.author.ilike(f'%{query}%')) |
            (Book.genre.ilike(f'%{query}%'))
        )
    if filter_genre:
        query_filter = query_filter.filter(Book.genre.ilike(f'%{filter_genre}%'))
    if filter_year:
        query_filter = query_filter.filter_by(publication_year=filter_year)
    if min_rating:
        query_filter = query_filter.having(Book.average_rating >= float(min_rating))

    books = query_filter.all()
    return jsonify([{'title': book.title, 'author': book.author, 'genre': book.genre, 'publication_year': book.publication_year, 'average_rating': book.average_rating} for book in books])