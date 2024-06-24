# editor : banyanrong
# time : 2024/6/23 16:39
from flask import Blueprint, request, jsonify
from app.services.activity_service import ActivityService
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import *

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/activities', methods=['POST'])
@jwt_required()
def add_activity():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        start_time = datetime.fromisoformat(data.get('start_time'))
        end_time = datetime.fromisoformat(data.get('end_time'))
        location = data.get('location')
        link = data.get('link')
        
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 401

        new_activity = ActivityService.add_activity(name, description, start_time, end_time, location, link)
        return jsonify({
            "message": "Activity added successfully",
            "activityId": new_activity.activity_id}), 201
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@activity_bp.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    try:
        activity = ActivityService.get_activity(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        return jsonify(activity.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@activity_bp.route('/activities', methods=['GET'])
def get_all_activities():
    try:
        activities = ActivityService.get_all_activities()
        if not activities:
            return jsonify({"error": "No activites found"}), 404
        return jsonify([activity.to_dict() for activity in activities]), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@activity_bp.route('/activities/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    start_time = datetime.fromisoformat(data.get('start_time'))
    end_time = datetime.fromisoformat(data.get('end_time'))
    location = data.get('location')
    link = data.get('link')

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        updated_activity = ActivityService.update_activity(activity_id, name, description, start_time, end_time, location, link)
        if updated_activity:
            return jsonify({"message": "Activity information updated successfully"}), 200
        return jsonify({'error': 'Activity not found'}), 404
    except:
        return jsonify({"error": "Unknown error occured"}), 404


@activity_bp.route('/activities/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    deleted_activity = ActivityService.delete_activity(activity_id)
    if deleted_activity:
        return jsonify({'message': 'Activity deleted successfully'}), 200
    return jsonify({'error': 'Activity not found'}), 404
