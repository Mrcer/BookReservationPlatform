import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import os
from abc import ABC, abstractmethod
import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "major"

db = SQLAlchemy(app)


class dbBook(db.Model):
    __tablename__ = "Book"
    book_id = db.Column(db.String(8), primary_key=True)
    book_name = db.Column(db.String(100))
    book_image = db.Column(db.LargeBinary(length=65536))
    book_author = db.Column(db.String(100))
    book_location = db.Column(db.String(100))
    book_score = db.Column(db.Float)
    book_storage = db.Column(db.String(50))
    book_reservation_time = db.Column(db.Float)
    book_reservation_location = db.Column(db.String(100))


class dbStudentAccount(db.Model):
    __tablename__ = "StudentAccount"
    net_id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100))
    gain = db.Column(db.Integer)
    password = db.Column(db.String(100))


class dbTeacherAccount(db.Model):
    __tablename__ = "TeacherAccount"
    net_id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100))
    real_name = db.Column(db.String(100))
    gain = db.Column(db.Integer)
    password = db.Column(db.String(100))


class dbAdminAccount(db.Model):
    __tablename__ = "AdminAccount"
    net_id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100))
    gain = db.Column(db.Integer)
    real_name = db.Column(db.String(100))
    password = db.Column(db.String(100))


class dbComment(db.Model):
    __tablename__ = "Comment"
    net_id = db.Column(db.String(8), primary_key=True)
    book_id = db.Column(db.String(8), primary_key=True)
    comment = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    time = db.Column(db.Float)


class dbReservationBook(db.Model):
    __tablename__ = "ReservationBook"
    net_id = db.Column(db.String(8), primary_key=True)
    book_id = db.Column(db.String(8), primary_key=True)
    time = db.Column(db.Float)


class dbBorrowBook(db.Model):
    __tablename__ = "BorrowBook"
    net_id = db.Column(db.String(8), primary_key=True)
    book_id = db.Column(db.String(8), primary_key=True)
    time = db.Column(db.Float)


class DataBase:
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.app = app
        self.db = db


class Account(ABC, DataBase):
    def __init__(self):
        super(Account, self).__init__()

    @abstractmethod
    def insert(self, args):
        pass

    """
        暂时只提供netid的查询接口
        net_id : '00000001'
        type : 'dbStudentAccount' | 'dbTeacherAccount' | 'dbAdminAccount'
    """

    def remove(self, net_id, type):
        res = eval(type).query.filter_by(net_id=net_id).first()
        self.db.session.delete(res)
        self.db.session.commit()
        self.db.session.close()

    """
    暂时只提供netid的查询接口
    net_id : '00000001'
    type : 'dbStudentAccount' | 'dbTeacherAccount' | 'dbAdminAccount'
    """

    def search(self, net_id, type):
        res = eval(type).query.filter_by(net_id=net_id).first()

        if res == None:
            return None

        if type == "dbStudentAccount":
            return {
                "net_id": res.net_id,
                "name": res.name,
                "gain": res.gain,
                "password": res.password,
            }
        elif type == "dbTeacherAccount" or type == "dbAdminAccount":
            return {
                "net_id": res.net_id,
                "name": res.name,
                "real_name": res.real_name,
                "gain": res.gain,
                "password": res.password,
            }

    """
    net_id : '00000001'
    update_content : {'id':xxx, 'name':xxx}
    type : 'dbStudentAccount' | 'dbTeacherAccount' | 'dbAdminAccount'
    """

    def update(self, net_id, update_content, type):
        eval(type).query.filter_by(net_id=net_id).update(update_content)
        self.db.session.commit()
        self.db.session.close()


class StudentAccount(Account):
    def __init__(self):
        super(StudentAccount, self).__init__()

    '''
    args : """
        {
            "net_id" : "00000001",
            "name" : "xiaohua",
            "gain" : 18,
            "password" : "abcdefg"
        }
           """
    '''

    def insert(self, args):
        args = json.loads(args)
        student = dbStudentAccount(
            net_id=args["net_id"],
            name=args["name"],
            gain=args["gain"],
            password=args["password"],
        )
        self.db.session.add(student)
        self.db.session.commit()
        self.db.session.close()


class TeacherAccount(Account):
    def __init__(self):
        super(TeacherAccount, self).__init__()

    '''
    args : """
        {
            "net_id" : "00000001",
            "name" : "xiaohua",
            "gain" : 18,
            "password" : "abcdefg"
        }
           """
    '''

    def insert(self, args):
        args = json.loads(args)
        teacher = dbTeacherAccount(
            net_id=args["net_id"],
            name=args["name"],
            real_name=args["real_name"],
            gain=args["gain"],
            password=args["password"],
        )
        self.db.session.add(teacher)
        self.db.session.commit()
        self.db.session.close()


class AdminAccount(Account):
    def __init__(self):
        super(AdminAccount, self).__init__()

    '''
    args : """
        {
            "net_id" : "00000001",
            "name" : "xiaohua",
            "gain" : 18,
            "password" : "abcdefg"
        }
           """
    '''

    def insert(self, args):
        args = json.loads(args)
        admin = dbAdminAccount(
            net_id=args["net_id"],
            name=args["name"],
            real_name=args["real_name"],
            gain=args["gain"],
            password=args["password"],
        )
        self.db.session.add(admin)
        self.db.session.commit()
        self.db.session.close()


class CommentAndBook(DataBase, ABC):
    def __init__(self):
        super(CommentAndBook, self).__init__()

    @abstractmethod
    def insert(self, args):
        pass

    """
        暂时只提供(net_id, book_id)的查询接口
        net_id : '00000001'
        book_id : '00000001'
        type : 'dbComment' | 'dbReservationBook' | 'dbBorrowBook'
    """

    def remove(self, net_id, book_id, type):
        res = eval(type).query.filter_by(net_id=net_id, book_id=book_id).first()
        self.db.session.delete(res)
        self.db.session.commit()
        self.db.session.close()

    """
        暂时只提供(net_id, book_id)的查询接口
        net_id : '00000001'
        book_id : '00000001'
        type : 'dbComment' | 'dbReservationBook' | 'dbBorrowBook'
    """

    def search(self, net_id, book_id, type):
        res = eval(type).query.filter_by(net_id=net_id, book_id=book_id).first()

        if res == None:
            return None

        if type == "dbComment":
            return {
                "net_id": res.net_id,
                "book_id": res.book_id,
                "comment": res.comment,
                "score": res.score,
                "time": res.time,
            }
        elif type == "dbReservationBook" or type == "dbBorrowBook":
            return {"net_id": res.net_id, "book_id": res.book_id, "time": res.time}

    """
        暂时只提供(net_id, book_id)的查询接口
        net_id : '00000001'
        book_id : '00000001'
        update_content : {'net_id' : '00000001'}
        type : 'dbComment' | 'dbReservationBook' | 'dbBorrowBook'
    """

    def update(self, net_id, book_id, update_content, type):
        eval(type).query.filter_by(net_id=net_id, book_id=book_id).update(
            update_content
        )
        self.db.session.commit()
        self.db.session.close()


class Comment(CommentAndBook):
    def __init__(self):
        super(Comment, self).__init__()

    '''
        args : """
            {
                "net_id" : "00000001",
                "name" : "xiaohua",
                "gain" : 18,
                "password" : "abcdefg"
            }
               """
    '''

    def insert(self, args):
        args = json.loads(args)
        comment = dbComment(
            net_id=args["net_id"],
            book_id=args["book_id"],
            comment=args["comment"],
            score=args["score"],
            time=args["time"],
        )
        self.db.session.add(comment)
        self.db.session.commit()
        self.db.session.close()


class ReservationBook(CommentAndBook):
    def __init__(self):
        super(ReservationBook, self).__init__()

    '''
        args : """
            {
                "net_id" : "00000001",
                "name" : "xiaohua",
                "gain" : 18,
                "password" : "abcdefg"
            }
               """
    '''

    def insert(self, args):
        args = json.loads(args)
        reservationBook = dbComment(
            net_id=args["net_id"], book_id=args["book_id"], time=args["time"]
        )
        self.db.session.add(reservationBook)
        self.db.session.commit()
        self.db.session.close()


class BorrowBook(CommentAndBook):
    def __init__(self):
        super(BorrowBook, self).__init__()

    def insert(self, args):
        args = json.loads(args)
        borrowBook = dbComment(
            net_id=args["net_id"], book_id=args["book_id"], time=args["time"]
        )
        self.db.session.add(borrowBook)
        self.db.session.commit()
        self.db.session.close()


class Book(DataBase):
    def __init__(self):
        super(Book, self).__init__()

    '''
        args : """
            {
                "net_id" : "00000001",
                "name" : "xiaohua",
                "gain" : 18,
                "password" : "abcdefg"
            }
               """
        image : 01bytes
    '''

    def insert(self, args, image):
        args = json.loads(args)
        book = dbBook(
            book_id=args["book_id"],
            book_name=args["book_name"],
            book_image=image,
            book_author=args["book_author"],
            book_location=args["book_location"],
            book_score=args["book_score"],
            book_storage=args["book_storage"],
            book_reservation_time=args["book_reservation_time"],
            book_reservation_location=args["book_reservation_location"],
        )
        self.db.session.add(book)
        self.db.session.commit()
        self.db.session.close()

    """
        暂时只提供book_id的查询接口
        book_id : '00000001'
    """

    def remove(self, book_id):
        res = dbBook.query.filter_by(book_id=book_id).first()
        self.db.session.delete(res)
        self.db.session.commit()
        self.db.session.close()

    """
        暂时只提供book_id的查询接口
        book_id : '00000001'
    """

    def search(self, book_id):
        res = dbBook.query.filter_by(book_id=book_id).first()

        if res == None:
            return None

        return {
            "book_id": res.book_id,
            "book_name": res.book_name,
            "book_image": res.book_image,
            "book_author": res.book_author,
            "book_location": res.book_location,
            "book_score": res.book_score,
            "book_storage": res.book_storage,
            "book_reservation_time": res.book_reservation_time,
            "book_reservation_location": res.book_reservation_location,
        }

    """
        暂时只提供book_id的查询接口
        book_id : '00000001'
        update_content : {'a': 'b', 'c': 'd'}
    """

    def update(self, book_id, update_content):
        dbBook.query.filter_by(book_id=book_id).update(update_content)
        self.db.session.commit()
        self.db.session.close()


if __name__ == "__main__":
    with app.app_context():
        # the use of account
        args = """
            {
                "net_id" : "00000001",
                "name" : "xiaohua",
                "gain" : 18,
                "password" : "abcdefg"
            }
            """
        StudentAccount().insert(args)
        res = StudentAccount().search("00000001", "dbStudentAccount")
        print(res)
        StudentAccount().update("00000001", {"gain": 80}, "dbStudentAccount")
        res = StudentAccount().search("00000001", "dbStudentAccount")
        print(res)
        StudentAccount().remove("00000001", "dbStudentAccount")
        res = StudentAccount().search("00000001", "dbStudentAccount")
        print(res)

        # the use of account and book state
        args = """
                {
                    "net_id" : "00000002",
                    "book_id" : "00001234",
                    "comment" : "this is a book.",
                    "score" : 90,
                    "time" : 1.23
                }
                """
        Comment().insert(args)
        res = Comment().search("00000002", "00001234", "dbComment")
        print(res)
        Comment().update(
            "00000002", "00001234", {"score": 100, "comment": "none"}, "dbComment"
        )
        res = Comment().search("00000002", "00001234", "dbComment")
        print(res)
        Comment().remove("00000002", "00001234", "dbComment")
        res = Comment().search("00000002", "00001234", "dbComment")
        print(res)

        args = """
                {
                    "book_id" : "00000001",
                    "book_name" : "book",
                    "book_author" : "others",
                    "book_location" : "west and east",
                    "book_score" : 3.4,
                    "book_storage" : "not reservation",
                    "book_reservation_time" : 1.1,
                    "book_reservation_location" : "the school"
                }
                """
        img = open(
            "img.png", "rb"
        ).read()  # img replace of the real path of your image to test
        Book().insert(args, img)
        res = Book().search("00000001")
        print(res["book_id"], res["book_author"])
        Book().update("00000001", {"book_author": "none"})
        res = Book().search("00000001")
        print(res["book_id"], res["book_author"])
        Book().remove("00000001")
        res = Book().search("00000001")
        print(res)
