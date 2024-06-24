from sqlalchemy import CheckConstraint
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)
    registration_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    role = db.Column(db.String(20), nullable=False)
    __table_args__ = (
        CheckConstraint("role IN ('student', 'teacher', 'admin')"),
    )

    reservations = db.relationship('Reservation', backref='users', lazy=True)
    reviews = db.relationship('Review', backref='users', lazy=True)
    scores = db.relationship('Score', backref='users', lazy=True)


class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    book_image = db.Column(db.LargeBinary)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    reservation_count = db.Column(db.Integer, default=0)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    __table_args__ = (
        CheckConstraint("status IN ('available', 'reserved', 'borrowed', 'damaged')"),
    )

    reservations = db.relationship('Reservation', backref='Book', lazy=True)
    reviews = db.relationship('Review', backref='Book', lazy=True)

    def average_rating(self):
        # 使用func.avg计算平均分，并使用scalar()直接返回结果
        average = db.session.query(func.avg(Review.rating)).filter(Review.book_id == self.book_id).scalar()
        # 如果没有评分，average将返回-1
        return float(average) if average is not None else -1

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    reservation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    status = db.Column(db.String(50), nullable=False)
    book_location = db.Column(db.String(50), nullable=False)
    reservation_location = db.Column(db.String(50), nullable=False)
    __table_args__ = (
        CheckConstraint("status IN ('confirmed', 'cancelled', 'completed', 'failed')"),
    )

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'reservation_date': self.reservation_date.isoformat(),
            'status': self.status,
            'book_location': self.book_location,
            'reservation_location': self.reservation_location
        }


class Review(db.Model):
    __tablename__ = "Review"
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5"),
    )

    def to_dict(self):
        return {
            'review_id': self.review_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'content': self.content,
            'rating': self.rating,
            'review_date': self.review_date.isoformat()
        }

class Score(db.Model):
    __tablename__ = "Score"
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    points = db.Column(db.Integer, nullable=False)
    change_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            'score_id': self.score_id,
            'user_id': self.user_id,
            'points': self.points,
            'change_date': self.change_date.isoformat(),
            'description': self.description
        }


class Activity(db.Model):
    __tablename__ = "Activity"
    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255))

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'name': self.name,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'location': self.location,
            'link': self.link
        }