# editor : banyanrong
# time : 2024/6/23 0:05
from flask import Blueprint, request, jsonify
from app.services.score_service import ScoreService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import *
score_bp = Blueprint('score_bp', __name__)


@score_bp.route('/scores', methods=['POST'])
def add_score():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        points = data.get('points')
        description = data.get('description')

        new_score = ScoreService.add_score(user_id, points, description)
        return jsonify({"message" : "Score added successfully",
                "scoreId" : new_score.score_id}), 201
    except Exception as e:
        return jsonify({"error": "Unauthorized"}), 404
    # return jsonify(new_score.score_id), 201


@score_bp.route('/scores/<int:user_id>', methods=['GET'])
def get_scores_by_user(user_id):
    try:
        scores = ScoreService.get_scores_by_user(user_id)
        if scores is not None:
            return jsonify([score.to_dict() for score in scores]), 200
        return jsonify({"error": "Score not found"}), 404
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@score_bp.route('/scores', methods=['GET'])
def get_scores():
    try:
        scores = ScoreService.get_scores()
        if scores is not None:
            return jsonify([score.to_dict() for score in scores]), 200
        return jsonify({"error": "No scores found"}), 404
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@score_bp.route('/scores/<int:score_id>', methods=['PUT'])
@jwt_required()
def update_score(score_id):
    data = request.get_json()
    points = data.get('points')
    description = data.get('description')

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    updated_score = ScoreService.update_score(score_id, points, description)
    try:
        if updated_score:
            return jsonify({"message": "Score information updated successfully"}), 200
            # return jsonify(updated_score.to_dict()), 200
        return jsonify({'error': 'Score not found'}), 404
    except Exception as e:
        return jsonify({'error': "Unknown error occured"}), 404


@score_bp.route('/scores/<int:score_id>', methods=['DELETE'])
@jwt_required()
def delete_score(score_id):
    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    deleted_score = ScoreService.delete_score(score_id)
    try:
        if deleted_score:
            return jsonify({'message': 'Score deleted successfully'}), 200
        return jsonify({'error': 'Score not found'}), 404
    except Exception as e:
        return jsonify({"message": "Unknown error occured"}), 404