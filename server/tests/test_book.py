from server.api import app,db
from flask_sqlalchemy import SQLAlchemy
import pytest


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内

with app.app_context():
    db.create_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
def test_get_book_info(client):
    # 测试获取图书信息
    response = client.get('/api/book?id=1')
    assert response.status_code == 200

    # 测试非法id
    response = client.get('/api/book?id=invalid_id')
    assert response.status_code == 400

def test_create_delete_book(client):
    # 测试创建图书
    response = client.post('/api/book', json={'id': 101, 'name': 'New Book'})
    assert response.status_code == 201

    # 测试删除图书
    response = client.delete('/api/book', json={'id': 101})
    assert response.status_code == 200