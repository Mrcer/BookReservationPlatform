# 测试函数
import requests
token = None
id = None

def test_user_registration():
    url = 'http://127.0.0.1:5000/api/users/register'
    user_data = {
        'username': 'newuser8',
        'password': 'password123',
        'email': 'newuser@example.com',
        'role': 'admin'
    }
    response = requests.post(url, json=user_data)
    print(response.json())

def test_user_login():
    global token
    global id
    url = 'http://127.0.0.1:5000/api/users/login'
    user_data = {
        'username': 'newuser8',
        'password': 'password123',
    }
    response = requests.post(url, json=user_data)
    token = response.json().get('token')
    id = response.json().get('userId')
    print(response.json())

def test_get_user_info():
    global token
    global id
    url = f'http://127.0.0.1:5000/api/users/{id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print(response.json())

def test_update_user_info():
    global token
    global id
    url = f'http://127.0.0.1:5000/api/users/{id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    user_data = {
        'email': 'updated_email@example.com'
    }
    response = requests.put(url, json=user_data, headers=headers)
    print(response.json())

def test_get_user_points():
    global token
    global id
    url = f'http://127.0.0.1:5000/api/users/{id}/points'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response =  requests.get(url, headers=headers)
    print(response.json())

def test_update_user_points():
    url = f'http://127.0.0.1:5000/api/users/{id}/points'
    headers = {
        'Authorization': f'Bearer {token}'  # 使用有效的管理员令牌
    }
    user_data = {
        'points': 100  # 假设的新积分值
    }
    response = requests.put(url, json=user_data, headers=headers)
    print(response.json())

def test_add_new_user():
    url = 'http://127.0.0.1:5000/api/admin/users'
    headers = {
        'Authorization': f'Bearer {token}'  # 使用有效的管理员令牌
    }
    new_user_data = {
        'username': 'newuser10',
        'password': 'newpassword123',
        'email': 'newuser10@example.com',
        'role': 'student'
    }
    response = requests.post(url, json=new_user_data, headers=headers)
    print(response.json())

def test_add_new_user():
    url = 'http://127.0.0.1:5000/api/admin/users'
    headers = {
        'Authorization': f'Bearer {token}'  # 使用有效的管理员令牌
    }
    new_user_data = {
        'username': 'newuser10',
        'password': 'newpassword123',
        'email': 'newuser10@example.com',
        'role': 'student'
    }
    response = requests.post(url, json=new_user_data, headers=headers)
    print(response.json())

def test_delete_user():
    url = f'http://127.0.0.1:5000/api/users/{id}'
    headers = {
        'Authorization': f'Bearer {token}'  # 使用有效的管理员令牌
    }
    response = requests.delete(url, headers=headers)
    print(response.json())

# 调用测试函数
test_user_registration()
test_user_login()
test_get_user_info()
# test_update_user_info()
test_get_user_points()
# test_update_user_points()
# test_get_user_points()
test_add_new_user()
test_delete_user()
test_get_user_info()