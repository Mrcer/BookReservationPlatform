# user_controller.py
from flask import Blueprint, request, jsonify
from app.services.user_service import *
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('user', __name__, url_prefix='/api')

@bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    result,status = register_user(data['username'], data['password'], data['email'], data['role'])
    return jsonify(result),status

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    result,status = login_user(data['username'], data['password'])
    return jsonify(result),status

@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    # 确保用户只能访问自己的信息，除非他们有更高权限（例如管理员）
    if current_user_id != user_id:
        return jsonify({'error': 'Access denied'}), 401

    user_info = get_user_by_id(user_id)
    if not user_info:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_info), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    result, status = update_user_info(user_id, data.get('email'))
    return jsonify(result), status

@bp.route('/users/<int:user_id>/points', methods=['GET'])
@jwt_required()
def get_user_points_route(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Access denied'}), 401

    points = get_user_points(user_id)
    if points is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'points': points}), 200

@bp.route('/users/<int:user_id>/points', methods=['PUT'])
@jwt_required()
def update_user_points(user_id):
    current_user_id = get_jwt_identity()
    current_user = get_user_by_id(current_user_id)
    if current_user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    points = data.get('points')
    if points is None:
        return jsonify({'error': 'No points provided'}), 400
    
    result, status = update_user_points_service(user_id, points)
    return jsonify(result), status

@bp.route('/admin/users', methods=['POST'])
@jwt_required()
def add_user():
    current_user_id = get_jwt_identity()
    current_user = get_user_by_id(current_user_id)
    if current_user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')
    email = user_data.get('email')
    role = user_data.get('role')

    result, status = register_user(username, password, email, role)
    result['message'] = 'User added successfully'
    return jsonify(result), status

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = get_user_by_id(current_user_id)
    if current_user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    result, status = delete_user(user_id)
    return jsonify(result), status

