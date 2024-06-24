import unittest
import sys
import os
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app_test, db
from app.models.model import *
from datetime import date

test_img = False #是否尝试显示图片看看图片编码解码是否正常

class BookTestCase(unittest.TestCase):
    

    def setUp(self):
        self.app = create_app_test()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # 添加一个模拟用户
            user1 = User(username='borrower', password="password", email="borrower@example.com", role="admin")
            user2 = User(username='reviewer1', password="password123", email="reviewer1@example.com", role="student")
            user3 = User(username='reviewer2', password="password456", email="reviewer2@example.com", role="student")
            db.session.add_all([user1, user2, user3])
            db.session.commit()

            from flask_jwt_extended import create_access_token
            self.access_token = create_access_token(identity=user1.user_id)
            
            # 读取图书封面图片，并编码为 Base64
            def get_book(image_path):
                with open(image_path, 'rb') as image_file:
                    return image_file.read()
            
            book1_image = get_book('tests/img.jpg')
            book2_image = get_book('tests/img.jpg')

            # 添加书籍
            book1 = Book(
                title='Test Book 1',
                author="Author 1",
                publisher="Publisher 1",
                publish_date=date.today(),
                isbn="1234567890",
                location="Shelf 1",
                status="available",
                reservation_count=3,
                borrower_id=None,
                book_image=book1_image  # 存储编码后的图片
            )
            book2 = Book(
                title='Test Book 2',
                author="Author 2",
                publisher="Publisher 2",
                publish_date=date.today(),
                isbn="0987654321",
                location="Shelf 2",
                status="borrowed",
                reservation_count=1,
                borrower_id=user1.user_id,
                book_image=book2_image  # 存储编码后的图片
            )
            db.session.add_all([book1, book2])
            db.session.commit()

            # 添加评分
            review1 = Review(user_id=user2.user_id, book_id=book1.book_id, content="Great book!", rating=5)
            review2 = Review(user_id=user3.user_id, book_id=book1.book_id, content="Good read, but a bit lengthy.", rating=4)
            db.session.add_all([review1, review2])
            db.session.commit()
            self.user_id = user1.user_id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_get_books(self):
        # 发送请求到API
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # 确保有数据返回
        self.assertIn('Test Book 1', str(data))  # 检查特定的书名是否在响应中

        # 尝试将返回的第一个图书的图像数据解码并显示
        if test_img and data and 'book_image' in data[0] and data[0]['book_image']:
            image_data = data[0]['book_image']
            # 解码Base64图像数据
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            plt.imshow(image)
            plt.axis('off')  # 不显示坐标轴
            plt.title("Img is working correctly.")
            plt.show()

        # 检查没有图书的情况
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error'], 'No books found')  # 确保正确的错误信息被返回

    def test_search_books(self):
        # 假设数据库中已有数据
        response = self.client.get('/api/books/search?query=Test')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # 检查是否返回了结果

        response = self.client.get('/api/books/search?query=nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('No books found for the given query', data['error'])

    def test_get_book_details(self):
        # 假设数据库中已有数据，这里的1应替换为实际的book_id
        response = self.client.get('/api/books/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)

        # 测试不存在的book_id
        response = self.client.get('/api/books/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('Book not found', data['error'])

    def test_get_book_status(self):
        # Testing existing book status
        response = self.client.get('/api/books/1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'available')

        # Testing non-existent book status
        response = self.client.get('/api/books/999/status')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['error'], 'Book not found')

    def test_get_borrowed_books(self):
        response = self.client.get(f'/api/books/borrowed/user/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)  # Expecting at least one borrowed book

        # Testing with a user that has no borrowed books

        response = self.client.get(f'/api/books/borrowed/user/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['error'], 'No borrowed books found for the user')

    def test_add_book(self):
        # Assuming admin_token is a valid JWT token for an admin user
        
        response = self.client.post('/api/books', json={
            'title': 'New Book',
            'author': 'New Author',
            'publisher': 'New Publisher',
            'publish_date': '2023-01-01',
            'isbn': '987654321',
            'location': 'New Shelf',
            'book_image': 'data:image/png;base64,iVBORw0KGgo='
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully', response.get_json()['message'])

    def test_update_book(self):
        # Assuming admin_token is a valid JWT token for an admin user
        # Assuming there is a book with book_id 1
        response = self.client.put('/api/books/1', json={
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publisher': 'Updated Publisher',
            'publish_date': '2023-10-01',
            'isbn': '1234567890',
            'location': 'Updated Shelf'
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book information updated successfully', response.get_json()['message'])
    
    def test_update_book_status(self):
        # Assuming access_token is a valid JWT token for an admin user
        response = self.client.put(f'/api/books/1/status', json={
            'status': 'available'
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book status updated successfully', response.get_json()['message'])
    
    def test_delete_book(self):
        # Assuming access_token is a valid JWT token for an admin user
        response = self.client.delete(f'/api/books/1', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted successfully', response.get_json()['message'])

        # Test for book not found
        response = self.client.delete(f'/api/books/9999', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Book not found', response.get_json()['error'])

    def test_create_book(self):
        # Assuming admin_token is a valid JWT token for an admin user

        response = self.client.post('/api/books', json={
            'title': 'New Book',
            'author': 'New Author',
            'publisher': 'New Publisher',
            'publish_date': '2023-01-01',
            'isbn': '987654321',
            'location': 'New Shelf',
            'book_image': 'data:image/png;base64,iVBORw0KGgo='
        }, headers={'Authorization': f'Bearer {self.access_token}'})

        book_id = response.json["bookId"]
        response = self.client.put(f'/api/books/{book_id}/borrow', json={
            'user_id': self.user_id
        }, headers={'Authorization': f'Bearer {self.access_token}'})

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
