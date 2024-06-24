from flask import Blueprint, request, jsonify
from app.services.reservation_service import ReservationService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import *

reservation_bp = Blueprint('reservation_bp', __name__)


@reservation_bp.route('/reservations', methods=['POST'])
@jwt_required()
def add_reservation():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    reservation_location = data.get('reservation_location')

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        new_reservation = ReservationService.add_reservation(user_id, book_id, reservation_location)
        if not new_reservation:
            return jsonify({"error": "Book not available for reservation"}), 404

        return jsonify({
            "message": "Reservation submitted successfully",
            "reservationId": new_reservation.reservation_id}), 201
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/<int:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        reservation = ReservationService.get_reservation(reservation_id)
        if reservation:
            return jsonify(reservation.to_dict()), 200
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/confirmed', methods=['GET'])
@jwt_required()
def get_all_confirmed_reservations():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        reservations = ReservationService.get_all_confirmed_reservations()
        if not reservations:
            return jsonify({"error": "No confirmed reservations found"}), 404
        return jsonify([reservation.to_dict() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_reservation_by_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401


    try:
        reservations = ReservationService.get_reservation_by_user(user_id)
        if not reservations:
            return jsonify({"error": "No reservations found for the user"}), 404
        return jsonify([reservation.to_dict() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_reservation_by_book(book_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401


    try:
        reservations = ReservationService.get_reservation_by_book(book_id)
        if not reservations:
            return jsonify({"error": "No reservations found for the book"}), 404
        return jsonify([reservation.to_dict() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/<int:reservation_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_reservation(reservation_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role not in ('student', 'teacher', 'admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        reservation = ReservationService.cancel_reservation(reservation_id)

        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404
        return jsonify({"message": "Reservation cancelled successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/<int:reservation_id>', methods=['PUT'])
@jwt_required()
def update_reservation(reservation_id):
    data = request.get_json()
    status = data.get('status')
    book_location = data.get('book_location')
    reservation_location = data.get('reservation_location')
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        updated_reservation = ReservationService.update_reservation(reservation_id, status, book_location, reservation_location)
        if updated_reservation:
            return jsonify({"message": "Reservation information updated successfully"}), 200
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/<int:reservation_id>/complete', methods=['PUT'])
@jwt_required()
def complete_reservation(reservation_id):
    data = request.get_json()
    pos_user_id = data.get('user_id')

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        reservation = ReservationService.complete_reservation(reservation_id, pos_user_id)

        if not reservation:
            return jsonify({"Reservation not found"}), 404

        return jsonify({"message": "Reservation completed successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404


@reservation_bp.route('/reservations/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(reservation_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        deleted_reservation = ReservationService.delete_reservation(reservation_id)
        if deleted_reservation:
            return jsonify({'message': 'Reservation deleted successfully'}), 200
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({"error": "Unknown error occured"}), 404

