from app.models.model import Reservation, Book, User, db
from . import reservation_points

class ReservationService:
    @staticmethod
    def add_reservation(user_id, book_id, reservation_location):
        book = Book.query.get(book_id)
        # if book.status != 'available':
        if book.status in ('borrowed', 'damaged'):
            return None
        user = User.query.get(user_id)
        if not user or user.points < reservation_points:
            return None
        book.status = 'reserved'
        book.reservation_count += 1
        db.session.commit()
        status = "confirmed"
        book_location = book.location
        new_reservation = Reservation(
            user_id=user_id,
            book_id=book_id,
            status=status,
            book_location=book_location,
            reservation_location=reservation_location
        )
        db.session.add(new_reservation)
        db.session.commit()
        return new_reservation

    @staticmethod
    def get_reservation(reservation_id):
        return Reservation.query.get(reservation_id)

    @staticmethod
    def get_all_confirmed_reservations():
        return Reservation.query.filter_by(status='confirmed').all()

    @staticmethod
    def get_reservation_by_user(user_id):
        return Reservation.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_reservation_by_book(book_id):
        return Reservation.query.filter_by(book_id=book_id).all()

    @staticmethod
    def cancel_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            reservation.status = 'cancelled'
            reservations = Reservation.query.filter_by(book_id=reservation.book_id).all()
            book_state = True
            book = Book.query.get(reservation.book_id)
            book.reservation_count -= 1
            for _reservation in reservations:
                if _reservation == 'confirmed':
                    book_state = False
                    break
            if book.status == 'reserved' and book_state:
                book.status = 'available'
                db.session.commit()
            db.session.commit()
        return reservation

    @staticmethod
    def update_reservation(reservation_id, status, book_location, reservation_location):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            reservation.status = status
            if status == 'confirmed':
                book = Book.query.get(reservation.book_id)
                if book.status == 'available':
                    book.status = 'reserved'
                    book.reservation_count += 1
                    db.session.commit()
            elif status == 'cancelled' or status == 'failed':
                book_state = True
                reservations = Reservation.query.filter_by(book_id=reservation.book_id).all()
                book = Book.query.get(reservation.book_id)
                book.reservation_count -= 1
                for _reservation in reservations:
                    if _reservation == 'confirmed':
                        book_state = False
                        break
                if book.status == 'reserved' and book_state:
                    book.status = 'available'
                    db.session.commit()
            elif status == 'completed':
                user = User.query.get(reservation.user_id)
                book = Book.query.get(reservation.book_id)
                book.reservation_count = 0
                user.points -= reservation_points
                # book.status = 'borrowed'
                db.session.commit()
                reservations = Reservation.query.filter_by(book_id=reservation.book_id).all()
                for _reservation in reservations:
                    if _reservation.status == 'confirmed':
                        _reservation.status = 'failed'
                        db.session.commit()
            reservation.book_location = book_location
            reservation.reservation_location = reservation_location
            db.session.commit()
        return reservation

    @staticmethod
    def complete_reservation(reservation_id, pos_user_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            reservation.status = 'completed'
            user = User.query.get(reservation.user_id)
            pos_user = User.query.get(pos_user_id)
            book = Book.query.get(reservation.book_id)
            book.reservation_count = 0
            user.points -= reservation_points
            pos_user.points += reservation_points
            # book.status = 'borrowed'
            db.session.commit()
            reservations = Reservation.query.filter_by(book_id=reservation.book_id).all()
            for _reservation in reservations:
                if _reservation.status == 'confirmed':
                    _reservation.status = 'failed'
                    db.session.commit()
        return reservation

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
        return reservation
