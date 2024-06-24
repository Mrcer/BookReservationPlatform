# book_service.py
from app import db
from app.models.model import *
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm.exc import NoResultFound
import base64
from dateutil import parser

def get_all_books():
    books = Book.query.all()
    return [
        {
            'bookId': book.book_id,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'publish_date': book.publish_date.strftime("%Y-%m-%d"),
            'isbn': book.isbn,
            'location': book.location,
            'status': book.status,
            'reservation_count': book.reservation_count,
            'borrower_id': book.borrower_id,
            'book_image': base64.b64encode(book.book_image).decode('utf-8') if book.book_image else None,
            'average_rating': book.average_rating()  
        }
        for book in books
    ]

def search_books(query):
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.publisher.ilike(f'%{query}%')) |
        (Book.isbn.ilike(f'%{query}%'))
    ).all()
    return [
        {
            'bookId': book.book_id,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'publish_date': book.publish_date.strftime("%Y-%m-%d"),
            'isbn': book.isbn,
            'location': book.location,
            'status': book.status,
            'reservation_count': book.reservation_count,
            'borrower_id': book.borrower_id,
            'book_image': base64.b64encode(book.book_image).decode('utf-8') if book.book_image else None,
            'average_rating': book.average_rating()  
        }
        for book in books
    ]

def get_book_by_id(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return None
    return {
        'bookId': book.book_id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'publish_date': book.publish_date.strftime("%Y-%m-%d"),
        'isbn': book.isbn,
        'location': book.location,
        'status': book.status,
        'reservation_count': book.reservation_count,
        'borrower_id': book.borrower_id,
        'book_image': base64.b64encode(book.book_image).decode('utf-8') if book.book_image else None,
        'average_rating': book.average_rating()  
    }

def get_book_status(book_id):
    book = db.session.get(Book, book_id)  
    if not book:
        return None
    return book.status

def get_borrowed_books_by_user(user_id):
    books = Book.query.filter_by(borrower_id=user_id).all()
    if not books:
        return []
    return [
        {
            'bookId': book.book_id,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'publish_date': book.publish_date.strftime("%Y-%m-%d"),
            'isbn': book.isbn,
            'location': book.location,
            'status': book.status,
            'borrower_id': book.borrower_id,
            'book_image': base64.b64encode(book.book_image).decode('utf-8') if book.book_image else None,
            'average_rating': book.average_rating() if hasattr(book, 'average_rating') else None
        }
        for book in books
    ]

def add_book(data):
    try:
        book_image_data = data.get('book_image', None)
        if isinstance(book_image_data, str) and ',' in book_image_data:
            # 提取Base64编码部分
            encoded_image = book_image_data.split(",", 1)[1]
        else:
            # 如果不包含逗号，认为整个字符串是Base64编码的数据或者直接返回None或错误
            encoded_image = book_image_data or ''

        book_image =  base64.b64decode(encoded_image)

        publish_date = parser.parse(data['publish_date']).date()

        new_book = Book(
            title=data['title'],
            author=data['author'],
            publisher=data['publisher'],
            publish_date=publish_date,
            isbn=data['isbn'],
            location=data['location'],
            status='available',  
            book_image=book_image
        )
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully', 'bookId': new_book.book_id}
    except Exception as e:
        return {'error': str(e)}
    
def update_book(book_id, data):
    book = Book.query.get(book_id)
    if not book:
        return {'error': 'Book not found'}
    publish_date = parser.parse(data['publish_date']).date()
    book_image_data = data.get('book_image', None)
    if isinstance(book_image_data, str) and ',' in book_image_data:
        # 提取Base64编码部分
        encoded_image = book_image_data.split(",", 1)[1]
    else:
        # 如果不包含逗号，认为整个字符串是Base64编码的数据或者直接返回None或错误
        encoded_image = book_image_data or ''

    book_image =  base64.b64decode(encoded_image)
    
    try:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.publisher = data.get('publisher', book.publisher)
        book.publish_date = publish_date
        book.isbn = data.get('isbn', book.isbn)
        book.location = data.get('location', book.location)
        book.book_image = book_image
        db.session.commit()
        return {'message': 'Book information updated successfully'}
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
    
def update_book_status(book_id, new_status):
    book = Book.query.get(book_id)
    if not book:
        return {'error': 'Book not found'}

    try:
        book.status = new_status
        db.session.commit()
        return {'message': 'Book status updated successfully'}
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
    
def delete_book_service(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {'error': 'Book not found'}

    try:
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}  
    
def update_book_borrow_service(book_id, user_id):
    book = Book.query.get(book_id)

    if not book:
        return {"error": 'Reservation not found'}
    try:
        book.status = 'borrowed'
        book.borrower_id = user_id
        db.session.commit()
        return {'message': 'Reservation completed successfully'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
    return book
    