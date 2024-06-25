# user_service.py
from app import db
from app.models.model import User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm.exc import NoResultFound

def register_user(username, password, email, role):
    hashed_password = generate_password_hash(password)
    # 首先检查用户名是否已经存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'error': 'Username already exists'}, 400
    
    # 如果用户名不存在，尝试创建新用户
    try:
        new_user = User(username=username, password=hashed_password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully', 'userId': new_user.user_id}, 201
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error'}, 400

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)
        return {
            'token': access_token, 
            'userId': user.user_id,
            'role': user.role
        }, 200
    else:
        return {'error': 'Invalid username or password'}, 401
    
def get_user_by_id(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).one()
        return {
            'userId': user.user_id,
            'username': user.username,
            'email': user.email,
            'points': user.points,
            'registration_date': user.registration_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化日期
            'role': user.role
        }
    except NoResultFound:
        return None
    
def update_user_info(user_id, email):
    try:
        user = User.query.filter_by(user_id=user_id).one()
        user.email = email
        db.session.commit()
        return {'message': 'User information updated successfully'}, 200
    except NoResultFound:
        return {'error': 'User not found'}, 404
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Email update failed'}, 400
    
def get_user_points(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None
    return user.points

def update_user_points_service(user_id, points):
    try:
        user = User.query.filter_by(user_id=user_id).one()
        user.points = points
        db.session.commit()
        return {'message': 'User points updated successfully'}, 200
    except NoResultFound:
        return {'error': 'User not found'}, 404
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400
    
def delete_user(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).one()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    except NoResultFound:
        return {'error': 'User not found'}, 404