import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import os
from abc import ABC, abstractmethod
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import json
from flask_cors import CORS
from datetime import datetime
from flask import request, jsonify
import pytz
import base64

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)  # 允许跨域名访问
# 配置 SQLAlchemy，指向本地 SQLite 数据库文件
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.sqlite"
)
# 用于指示是否追踪对象的修改并发送信号给 Flask 应用程序
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 设置 Flask 应用的密钥，用于保持客户端会话的安全
app.config["SECRET_KEY"] = "major"

db = SQLAlchemy(app)


# 定义数据库模型
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

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class dbReservationBook(db.Model):
    __tablename__ = "ReservationBook"
    net_id = db.Column(db.String(8), primary_key=True)
    book_id = db.Column(db.String(8), primary_key=True)
    time = db.Column(db.Float)

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class dbBorrowBook(db.Model):
    __tablename__ = "BorrowBook"
    net_id = db.Column(db.String(8), primary_key=True)
    book_id = db.Column(db.String(8), primary_key=True)
    time = db.Column(db.DateTime)


class DataBase:
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.app = app
        self.db = db


def insert_account(account_data, account_class):
    account = account_class(**json.loads(account_data))
    db.session.add(account)
    db.session.commit()
    return {"message": "Account created successfully"}


# 通用功能，用于获取账户信息
def get_account(net_id, account_class):
    account = account_class.query.filter_by(net_id=net_id).first()
    if account:
        return {
            "net_id": account.net_id,
            "name": account.name,
            "real_name": getattr(account, "real_name", None),
            "gain": account.gain,
            "password": account.password,
        }
    else:
        return {"message": "Account not found"}, 404


# 通用功能，用于更新账户信息
def update_account(net_id, update_content, account_class):
    account = account_class.query.filter_by(net_id=net_id).update(
        json.loads(update_content)
    )
    db.session.commit()
    return {"message": "Account updated successfully"}


# 通用功能，用于删除账户信息
def delete_account(net_id, account_class):
    account = account_class.query.filter_by(net_id=net_id).first()
    if account:
        db.session.delete(account)
        db.session.commit()
        return {"message": "Account deleted successfully"}
    else:
        return {"message": "Account not found"}, 404


# 通用功能，用于删除账户信息
def generic_insert(args, model):
    item = model(**json.loads(args))
    db.session.add(item)
    db.session.commit()
    return {"message": "Item created successfully"}


def generic_get(net_id, book_id, model):
    item = model.query.filter_by(net_id=net_id, book_id=book_id).first()
    if item:
        return item.as_dict()
    else:
        return {"message": "Item not found"}, 404


def generic_delete(net_id, book_id, model):
    item = model.query.filter_by(net_id=net_id, book_id=book_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}, 404


# RESTful API 端点定义，用于创建、获取、更新和删除学生账户
@app.route("/account/student", methods=["POST"])
def create_student_account():
    """
    创建学生账户的API端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "student123",
        "name": "John Doe",
        "gain": 100,
        "password": "password123"
    }

    返回结果:
    成功创建账户时返回:
    {
        "message": "Account created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    return jsonify(insert_account(request.data, dbStudentAccount))


@app.route("/account/student/<net_id>", methods=["GET"])
def get_student_account(net_id):
    """
    获取指定学生账户信息的API端点。

    请求方法: GET
    路径参数:
    - net_id: 学生的网络ID

    返回结果:
    如果找到指定的学生账户，返回账户信息，格式如下:
    {
        "net_id": "student123",
        "name": "John Doe",
        "real_name": null,  # 如果账户类型没有real_name字段，返回null
        "gain": 100,
        "password": "password123"
    }

    如果找不到指定的学生账户，返回404错误。
    """
    return jsonify(get_account(net_id, dbStudentAccount))


@app.route("/account/student/<net_id>", methods=["PUT"])
def update_student_account(net_id):
    """
    更新指定学生账户信息的API端点。

    请求方法: PUT
    路径参数:
    - net_id: 学生的网络ID
    请求体数据格式: JSON
    请求体数据示例:
    {
        "name": "Updated Name",
        "gain": 150
    }

    返回结果:
    成功更新账户信息时返回:
    {
        "message": "Account updated successfully"
    }

    如果找不到指定的学生账户，返回404错误。
    """
    return jsonify(update_account(net_id, request.data, dbStudentAccount))


@app.route("/account/student/<net_id>", methods=["DELETE"])
def delete_student_account(net_id):
    """
    删除指定学生账户的API端点。

    请求方法: DELETE
    路径参数:
    - net_id: 学生的网络ID

    返回结果:
    成功删除账户时返回:
    {
        "message": "Account deleted successfully"
    }

    如果找不到指定的学生账户，返回404错误。
    """
    return jsonify(delete_account(net_id, dbStudentAccount))


# RESTful API 端点定义，用于创建、获取、更新和删除教师账户
@app.route("/account/teacher", methods=["POST"])
def create_teacher_account():
    """
    创建教师账户的API端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "teacher123",
        "name": "Jane Smith",
        "real_name": "Jane Doe",  # 可选字段
        "gain": 200,
        "password": "password456"
    }

    返回结果:
    成功创建账户时返回:
    {
        "message": "Account created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    return jsonify(insert_account(request.data, dbTeacherAccount))


@app.route("/account/teacher/<net_id>", methods=["GET"])
def get_teacher_account(net_id):
    """
    获取指定教师账户信息的API端点。

    请求方法: GET
    路径参数:
    - net_id: 教师的网络ID

    返回结果:
    如果找到指定的教师账户，返回账户信息，格式如下:
    {
        "net_id": "teacher123",
        "name": "Jane Smith",
        "real_name": "Jane Doe",  # 如果账户类型有real_name字段，返回真实姓名
        "gain": 200,
        "password": "password456"
    }

    如果找不到指定的教师账户，返回404错误。
    """
    return jsonify(get_account(net_id, dbTeacherAccount))


@app.route("/account/teacher/<net_id>", methods=["PUT"])
def update_teacher_account(net_id):
    """
    更新指定教师账户信息的API端点。

    请求方法: PUT
    路径参数:
    - net_id: 教师的网络ID
    请求体数据格式: JSON
    请求体数据示例:
    {
        "name": "Updated Name",
        "gain": 250
    }

    返回结果:
    成功更新账户信息时返回:
    {
        "message": "Account updated successfully"
    }

    如果找不到指定的教师账户，返回404错误。
    """
    return jsonify(update_account(net_id, request.data, dbTeacherAccount))


@app.route("/account/teacher/<net_id>", methods=["DELETE"])
def delete_teacher_account(net_id):
    """
    删除指定教师账户的API端点。

    请求方法: DELETE
    路径参数:
    - net_id: 教师的网络ID

    返回结果:
    成功删除账户时返回:
    {
        "message": "Account deleted successfully"
    }

    如果找不到指定的教师账户，返回404错误。
    """
    return jsonify(delete_account(net_id, dbTeacherAccount))


# RESTful API 端点定义，用于创建、获取、更新和删除管理员账户
@app.route("/account/admin", methods=["POST"])
def create_admin_account():
    """
    创建管理员账户的API端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "admin123",
        "name": "Admin User",
        "gain": 300,
        "real_name": "Admin Doe",  # 可选字段
        "password": "password789"
    }

    返回结果:
    成功创建账户时返回:
    {
        "message": "Account created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    return jsonify(insert_account(request.data, dbAdminAccount))


@app.route("/account/admin/<net_id>", methods=["GET"])
def get_admin_account(net_id):
    """
    获取指定管理员账户信息的API端点。

    请求方法: GET
    路径参数:
    - net_id: 管理员的网络ID

    返回结果:
    如果找到指定的管理员账户，返回账户信息，格式如下:
    {
        "net_id": "admin123",
        "name": "Admin User",
        "real_name": "Admin Doe",  # 如果账户类型有real_name字段，返回真实姓名
        "gain": 300,
        "password": "password789"
    }

    如果找不到指定的管理员账户，返回404错误。
    """
    return jsonify(get_account(net_id, dbAdminAccount))


@app.route("/account/admin/<net_id>", methods=["PUT"])
def update_admin_account(net_id):
    """
    更新指定管理员账户信息的API端点。

    请求方法: PUT
    路径参数:
    - net_id: 管理员的网络ID
    请求体数据格式: JSON
    请求体数据示例:
    {
        "name": "Updated Admin Name",
        "gain": 350
    }

    返回结果:
    成功更新账户信息时返回:
    {
        "message": "Account updated successfully"
    }

    如果找不到指定的管理员账户，返回404错误。
    """
    return jsonify(update_account(net_id, request.data, dbAdminAccount))


@app.route("/account/admin/<net_id>", methods=["DELETE"])
def delete_admin_account(net_id):
    """
    删除指定管理员账户的API端点。

    请求方法: DELETE
    路径参数:
    - net_id: 管理员的网络ID

    返回结果:
    成功删除账户时返回:
    {
        "message": "Account deleted successfully"
    }

    如果找不到指定的管理员账户，返回404错误。
    """
    return jsonify(delete_account(net_id, dbAdminAccount))


# 评论 API
@app.route("/comments", methods=["POST"])
def create_comment():
    """
    创建评论的API端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "user123",
        "book_id": "book456",
        "comment": "This book is great!",
        "score": 5,
        "time": 1645612345.678  # 时间戳，表示评论时间
    }

    返回结果:
    成功创建评论时返回:
    {
        "message": "Item created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    return jsonify(generic_insert(request.data, dbComment))


@app.route("/comments/<net_id>/<book_id>", methods=["GET"])
def get_comment(net_id, book_id):
    """
    获取指定用户对指定图书的评论信息的API端点。

    请求方法: GET
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    如果找到指定的评论，返回评论信息，格式如下:
    {
        "net_id": "user123",
        "book_id": "book456",
        "comment": "This book is great!",
        "score": 5,
        "time": 1645612345.678
    }

    如果找不到指定的评论，返回404错误。
    """
    return jsonify(generic_get(net_id, book_id, dbComment))


@app.route("/comments/<net_id>/<book_id>", methods=["DELETE"])
def delete_comment(net_id, book_id):
    """
    删除指定用户对指定图书的评论的API端点。

    请求方法: DELETE
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    成功删除评论时返回:
    {
        "message": "Item deleted successfully"
    }

    如果找不到指定的评论，返回404错误。
    """
    return jsonify(generic_delete(net_id, book_id, dbComment))


# 预约 API
@app.route("/reservations", methods=["POST"])
def create_reservation():
    """
    创建预约的API端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "user123",
        "book_id": "book456",
        "time": 1645612345.678  # 时间戳，表示预约时间
    }

    返回结果:
    成功创建预约时返回:
    {
        "message": "Item created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    return jsonify(generic_insert(request.data, dbReservationBook))


@app.route("/reservations/<net_id>/<book_id>", methods=["GET"])
def get_reservation(net_id, book_id):
    """
    获取指定用户对指定图书的预约信息的API端点。

    请求方法: GET
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    如果找到指定的预约，返回预约信息，格式如下:
    {
        "net_id": "user123",
        "book_id": "book456",
        "time": 1645612345.678
    }

    如果找不到指定的预约，返回404错误。
    """
    return jsonify(generic_get(net_id, book_id, dbReservationBook))


@app.route("/reservations/<net_id>/<book_id>", methods=["DELETE"])
def delete_reservation(net_id, book_id):
    """
    删除指定用户对指定图书的预约的API端点。

    请求方法: DELETE
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    成功删除预约时返回:
    {
        "message": "Item deleted successfully"
    }

    如果找不到指定的预约，返回404错误。
    """
    return jsonify(generic_delete(net_id, book_id, dbReservationBook))


# 借书api
@app.route("/borrowbook", methods=["POST"])
def create_borrow_book():
    """
    创建借书记录的 API 端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "net_id": "user123",
        "book_id": "book456",
        "time": "2024-06-16T12:00:00Z"  # ISO 8601 格式的时间字符串，表示借书时间
    }

    返回结果:
    成功创建借书记录时返回:
    {
        "message": "Borrow book record created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    data = request.get_json()
    net_id = data["net_id"]
    book_id = data["book_id"]
    time_str = data["time"]
    time = datetime.fromisoformat(
        time_str.replace("Z", "+00:00")
    )  # Correct parsing of ISO 8601 strings

    borrow_book = dbBorrowBook(net_id=net_id, book_id=book_id, time=time)
    db.session.add(borrow_book)
    db.session.commit()
    return jsonify({"message": "Borrow book record created successfully"}), 201


@app.route("/borrowbook/<net_id>/<book_id>", methods=["GET"])
def get_borrow_book(net_id, book_id):
    """
    获取指定用户对指定图书的借书记录的 API 端点。

    请求方法: GET
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    如果找到指定的借书记录，返回借书记录信息，格式如下:
    {
        "net_id": "user123",
        "book_id": "book456",
        "time": "2024-06-16T12:00:00Z"  # ISO 8601 格式的时间字符串，表示借书时间
    }

    如果找不到指定的借书记录，返回404错误。
    """
    borrow_book = dbBorrowBook.query.filter_by(net_id=net_id, book_id=book_id).first()
    if borrow_book:
        return jsonify(
            {
                "net_id": borrow_book.net_id,
                "book_id": borrow_book.book_id,
                "time": borrow_book.time,
            }
        )
    return jsonify({"message": "Borrow book record not found"}), 404


@app.route("/borrowbook/<net_id>/<book_id>", methods=["DELETE"])
def delete_borrow_book(net_id, book_id):
    """
    删除指定用户对指定图书的借书记录的 API 端点。

    请求方法: DELETE
    路径参数:
    - net_id: 用户的网络ID
    - book_id: 图书的ID

    返回结果:
    成功删除借书记录时返回:
    {
        "message": "Borrow book record deleted successfully"
    }

    如果找不到指定的借书记录，返回404错误。
    """
    borrow_book = dbBorrowBook.query.filter_by(net_id=net_id, book_id=book_id).first()
    if borrow_book:
        db.session.delete(borrow_book)
        db.session.commit()
        return jsonify({"message": "Borrow book record deleted successfully"})
    return jsonify({"message": "Borrow book record not found"}), 404


# 书的相关操作api
@app.route("/books", methods=["POST"])
def create_book():
    """
    创建书籍记录的 API 端点。

    请求方法: POST
    请求体数据格式: JSON
    请求体数据示例:
    {
        "book_id": "book123",
        "book_name": "Python Programming",
        "book_image": "<base64_encoded_image_data>",  # 图书封面的 Base64 编码字符串，可选
        "book_author": "Guido van Rossum",
        "book_location": "Library A",
        "book_score": 4.5,
        "book_storage": "Shelf B",
        "book_reservation_time": 3600.0,
        "book_reservation_location": "Desk 1"
    }

    返回结果:
    成功创建书籍记录时返回:
    {
        "message": "Book created successfully"
    }

    如果请求体数据不完整或格式不正确，将返回400错误。
    """
    data = request.get_json()
    try:
        # If book_image is a base64 string, decode it
        if data["book_image"]:
            book_image = base64.b64decode(data["book_image"])
        else:
            book_image = None

        book = dbBook(
            book_id=data["book_id"],
            book_name=data["book_name"],
            book_image=book_image,  # Use the binary data
            book_author=data["book_author"],
            book_location=data["book_location"],
            book_score=data["book_score"],
            book_storage=data["book_storage"],
            book_reservation_time=data["book_reservation_time"],
            book_reservation_location=data["book_reservation_location"],
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    """
    获取指定书籍信息的 API 端点。

    请求方法: GET
    路径参数:
    - book_id: 图书的ID

    返回结果:
    如果找到指定的书籍，返回书籍信息，格式如下:
    {
        "book_id": "book123",
        "book_name": "Python Programming",
        "book_image": "<base64_encoded_image_data>",  # 图书封面的 Base64 编码字符串，可选
        "book_author": "Guido van Rossum",
        "book_location": "Library A",
        "book_score": 4.5,
        "book_storage": "Shelf B",
        "book_reservation_time": 3600.0,
        "book_reservation_location": "Desk 1"
    }

    如果找不到指定的书籍，返回404错误。
    """
    book = dbBook.query.filter_by(book_id=book_id).first()
    if book:
        return jsonify(
            {
                "book_id": book.book_id,
                "book_name": book.book_name,
                "book_image": book.book_image,
                "book_author": book.book_author,
                "book_location": book.book_location,
                "book_score": book.book_score,
                "book_storage": book.book_storage,
                "book_reservation_time": book.book_reservation_time,
                "book_reservation_location": book.book_reservation_location,
            }
        )
    return jsonify({"message": "Book not found"}), 404


@app.route("/books/<book_id>", methods=["PUT"])
def update_book(book_id):
    """
    更新指定书籍信息的 API 端点。

    请求方法: PUT
    路径参数:
    - book_id: 图书的ID
    请求体数据格式: JSON
    请求体数据示例:
    {
        "book_name": "Updated Python Programming",
        "book_author": "Updated Author",
        "book_location": "Updated Library A",
        "book_score": 4.7,
        "book_storage": "Updated Shelf B",
        "book_reservation_time": 7200.0,
        "book_reservation_location": "Updated Desk 2"
    }

    返回结果:
    成功更新书籍信息时返回:
    {
        "message": "Book updated successfully"
    }

    如果找不到指定的书籍，返回404错误。
    """
    data = request.get_json()
    dbBook.query.filter_by(book_id=book_id).update(data)
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})


@app.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    删除指定书籍的 API 端点。

    请求方法: DELETE
    路径参数:
    - book_id: 图书的ID

    返回结果:
    成功删除书籍时返回:
    {
        "message": "Book deleted successfully"
    }

    如果找不到指定的书籍，返回404错误。
    """
    book = dbBook.query.filter_by(book_id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"message": "Book not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
