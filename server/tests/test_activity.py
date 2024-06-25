# editor : banyanrong
# time : 2024/6/23 16:40
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app_test, db
from app.models.model import Activity,User
from datetime import date

class ActivityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app_test()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', password="123456", email="123@163.com", role="admin")
            db.session.add(user)
            db.session.commit()
            from flask_jwt_extended import create_access_token
            self.access_token = create_access_token(identity=user.user_id)
            

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_add_activity(self):
        response = self.client.post('/api/activities', json={
            'name': 'Test Activity',
            'description': 'This is a test activity',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location',
            'link': 'http://testlink.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 201)

    def test_get_activity(self):
        response = self.client.post('/api/activities', json={
            'name': 'Test Activity',
            'description': 'This is a test activity',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location',
            'link': 'http://testlink.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        activity_id = response.json['activityId']
        response = self.client.get(f'/api/activities/{activity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Activity', response.get_data(as_text=True))

    def test_get_all_activities(self):
        self.client.post('/api/activities', json={
            'name': 'Test Activity 1',
            'description': 'This is a test activity 1',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location 1',
            'link': 'http://testlink1.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.client.post('/api/activities', json={
            'name': 'Test Activity 2',
            'description': 'This is a test activity 2',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location 2',
            'link': 'http://testlink2.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        response = self.client.get('/api/activities')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 2)

    def test_update_activity(self):
        response = self.client.post('/api/activities', json={
            'name': 'Test Activity',
            'description': 'This is a test activity',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location',
            'link': 'http://testlink.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        activity_id = response.json["activityId"]
        response = self.client.put(f'/api/activities/{activity_id}', json={
            'name': 'Updated Activity',
            'description': 'This is an updated test activity',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Updated Location',
            'link': 'http://updatedlink.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Activity information updated successfully")

    def test_delete_activity(self):
        response = self.client.post('/api/activities', json={
            'name': 'Test Activity',
            'description': 'This is a test activity',
            'start_time': date.today().isoformat(),
            'end_time': date.today().isoformat(),
            'location': 'Test Location',
            'link': 'http://testlink.com',
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        activity_id = response.json["activityId"]
        response = self.client.delete(f'/api/activities/{activity_id}', json={
        }, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/activities/{activity_id}', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
