# editor : banyanrong
# time : 2024/6/23 14:54
from flask import Blueprint, request, jsonify
from app.services.review_service import ReviewService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import *

review_bp = Blueprint('review_bp', __name__)


@review_bp.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    data = request.get_json()
    user_id = data.get('userId')
    book_id = data.get('bookId')
    content = data.get('content')
    rating = data.get('rating')

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        new_review = ReviewService.add_review(user_id, book_id, content, rating)
        return jsonify({"message": "Review added successfully", "reviewId": new_review.review_id}), 201
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews/books/<int:book_id>/rating', methods=['GET'])
def get_book_rating(book_id):
    try:
        rating = ReviewService.get_book_rating(book_id)
        if not rating:
            return jsonify({"error": "Book not found"}), 404
        return jsonify({
            "bookId": book_id,
            "average_rating": rating}), 200
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        reviews = ReviewService.get_reviews()
        if not reviews:
            return jsonify({"error": "No reviews found"}), 404
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_reviews_by_review(review_id):
    try:
        reviews = ReviewService.get_reviews_by_review(review_id)
        if not reviews:
            return jsonify({"error": "No reviews found"}), 404
        return jsonify(reviews[0].to_dict()), 200
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews/books/<int:book_id>/reviews', methods=['GET'])
def get_reviews_by_book(book_id):
    reviews = ReviewService.get_reviews_by_book(book_id)
    try:
        if not reviews:
            return jsonify({"error": "No reviews found for the book"}), 404
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        updated_review = ReviewService.update_review(review_id, content, rating)
        if updated_review:
            return jsonify({"message": "Review information updated successfully"}), 200
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404


@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        deleted_review = ReviewService.delete_review(review_id)
        if deleted_review:
            return jsonify({'message': 'Review deleted successfully'}), 200
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404
