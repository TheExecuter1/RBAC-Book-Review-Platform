from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Comment

comments_blueprint = Blueprint('comments', __name__)

@comments_blueprint.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    data = request.get_json()
    review_id = data.get('review_id')
    text = data.get('text')

    if not review_id or not text:
        return jsonify({'message': 'Review ID and text are required'}), 400
    
    comment = Comment(review_id=data['review_id'], user_id=user_id, text=data['text'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

@comments_blueprint.route('/comments/<int:review_id>', methods=['GET'])
def get_comments(review_id):
    comments = Comment.query.filter_by(review_id=review_id).all()
    return jsonify([{'user_id': comment.user_id, 'text': comment.text, 'created_at': comment.created_at} for comment in comments])


@comments_blueprint.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()

    if comment is None:
        return jsonify({'message': 'Comment not found or access denied'}), 404

    data = request.get_json()
    comment.text = data.get('text', comment.text)
    db.session.commit()

    return jsonify({'message': 'Comment updated successfully'}), 200

@comments_blueprint.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()

    if comment is None:
        return jsonify({'message': 'Comment not found or access denied'}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'}), 200