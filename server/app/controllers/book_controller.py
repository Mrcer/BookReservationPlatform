# book_controller.py
from flask import Blueprint, request, jsonify
from app.services.book_service import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from base64 import b64encode

bp = Blueprint('book', __name__, url_prefix='/api/books')

@bp.route('', methods=['GET'])
def get_books():
    books = get_all_books()
    if not books:
        return jsonify({'error': 'No books found'}), 404
    return jsonify(books), 200

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # 获取查询参数
    books = search_books(query)
    if not books:
        return jsonify({'error': 'No books found for the given query'}), 404
    return jsonify(books), 200

@bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book), 200

@bp.route('/<int:book_id>/status', methods=['GET'])
def book_status(book_id):
    status = get_book_status(book_id)
    if status is None:
        return jsonify({'error': 'Book not found'}),404
    return jsonify({'status': status}), 200

@bp.route('/borrowed/user/<int:user_id>', methods=['GET'])
def borrowed_books(user_id):
    books = get_borrowed_books_by_user(user_id)
    if not books:
        return jsonify({'error': 'No borrowed books found for the user'}), 404
    return jsonify(books), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    result = add_book(data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201

@bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book_info(book_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    result = update_book(book_id, data)
    if 'error' in result:
        return jsonify(result), 404 if result['error'] == 'Book not found' else 400
    return jsonify(result), 200

@bp.route('/<int:book_id>/status', methods=['PUT'])
@jwt_required()
def update_status(book_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    result = update_book_status(book_id, data.get('status'))
    if 'error' in result:
        return jsonify(result), 404 if result['error'] == 'Book not found' else 400
    return jsonify(result), 200

@bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book_endpoint(book_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    result = delete_book_service(book_id)
    if result.get('error'):
        status_code = 404 if result['error'] == 'Book not found' else 400
        return jsonify(result), status_code
    return jsonify(result), 200

@bp.route('<int:book_id>/borrow', methods=['PUT'])
@jwt_required()
def update_book_borrow(book_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error':'Unauthorized'}), 401

    data = request.get_json()
    user_id = data.get("user_id")
    result = update_book_borrow_service(book_id, user_id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result), 200