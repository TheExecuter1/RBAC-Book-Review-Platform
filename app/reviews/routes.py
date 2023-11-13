from flask import Blueprint, request, jsonify
from app import db
from .models import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_blueprint = Blueprint('reviews', __name__)

@reviews_blueprint.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    rating = data.get('rating')
    text = data.get('text')

    if not book_id or rating is None or not text:
        return jsonify({'message': 'Book ID, rating, and text are required'}), 400
    
    review = Review(book_id=data['book_id'], user_id=user_id, rating=data['rating'], text=data['text'])
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully'}), 201

@reviews_blueprint.route('/reviews/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([{'rating': review.rating, 'text': review.text, 'created_at': review.created_at} for review in reviews])


@reviews_blueprint.route('/rate_book', methods=['POST'])
@jwt_required()
def rate_book():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    rating = data.get('rating')

    review = Review(user_id=user_id, book_id=book_id, rating=rating, text="")
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Rating submitted successfully'}), 201


@reviews_blueprint.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def edit_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.filter_by(id=review_id, user_id=user_id).first()

    if review is None:
        return jsonify({'message': 'Review not found or access denied'}), 404

    data = request.get_json()
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)
    db.session.commit()

    return jsonify({'message': 'Review updated successfully'}), 200

@reviews_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.filter_by(id=review_id, user_id=user_id).first()

    if review is None:
        return jsonify({'message': 'Review not found or access denied'}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully'}), 200