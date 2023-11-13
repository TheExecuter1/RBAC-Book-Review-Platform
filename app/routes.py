from flask import Blueprint, request, jsonify
from app import db
from app.models import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_blueprint = Blueprint('reviews', __name__)

@reviews_blueprint.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    review = Review(book_id=data['book_id'], user_id=user_id, rating=data['rating'], text=data['text'])
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully'}), 201

@reviews_blueprint.route('/reviews/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([{'rating': review.rating, 'text': review.text, 'created_at': review.created_at} for review in reviews])
