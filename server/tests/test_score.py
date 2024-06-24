import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models.model import Score, User


class ScoreTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', password="123456", email="123@163.com", role="admin")
            db.session.add(user)
            db.session.commit()
            from flask_jwt_extended import create_access_token
            self.access_token = create_access_token(identity=user.user_id)
            self.user_id = user.user_id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_add_score(self):
        response = self.client.post('/api/scores', json={
            'user_id': self.user_id,
            'points': 10,
            'description': 'Initial score'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_scores_by_user(self):
        self.client.post('/api/scores', json={
            'user_id': self.user_id,
            'points': 10,
            'description': 'Initial score'
        })
        response = self.client.get(f'/api/scores/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_scores(self):
        self.client.post('/api/scores', json={
            'user_id': self.user_id,
            'points' : 20,
            'description': 'Initial score'
        })
        response = self.client.get(f'/api/scores')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_update_score(self):
        response = self.client.post('/api/scores', json={
            'user_id': self.user_id,
            'points': 10,
            'description': 'Initial score'
        })
        score_id = response.json
        response = self.client.put(f'/api/scores/{score_id["scoreId"]}', json={
            'points': 20,
            'description': 'Updated score',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Score information updated successfully")

    def test_delete_score(self):
        response = self.client.post('/api/scores', json={
            'user_id': self.user_id,
            'points': 10,
            'description': 'Initial score'
        })
        score_id = response.json
        response = self.client.delete(f'/api/scores/{score_id["scoreId"]}', json={
            'authorization': "admin"
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
