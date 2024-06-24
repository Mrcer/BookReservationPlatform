# editor : banyanrong
# time : 2024/6/23 14:54
from app.models.model import Review, db

class ReviewService:
    @staticmethod
    def add_review(user_id, book_id, content, rating):
        new_review = Review(user_id=user_id, book_id=book_id, content=content, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        return new_review

    @staticmethod
    def get_reviews():
        return Review.query.all()

    @staticmethod
    def get_reviews_by_review(review_id):
        return Review.query.filter_by(review_id=review_id).all()

    @staticmethod
    def get_reviews_by_book(book_id):
        return Review.query.filter_by(book_id=book_id).all()

    @staticmethod
    def get_book_rating(book_id):
        reviews = Review.query.filter_by(book_id=book_id).all()
        if reviews:
            rating = 0
            for _review in reviews:
                rating += _review.rating
            return rating / len(reviews)
        return reviews

    @staticmethod
    def update_review(review_id, content, rating):
        review = Review.query.get(review_id)
        if review:
            review.content = content
            review.rating = rating
            db.session.commit()
        return review

    @staticmethod
    def delete_review(review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
        return review
