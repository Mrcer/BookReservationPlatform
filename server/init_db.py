import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# 常规数据库创建

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    points INT DEFAULT 10,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT CHECK(role IN ('student', 'teacher', 'admin')) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE Book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    book_image BLOB,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    publish_date DATE NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    location VARCHAR(50) NOT NULL,
    status TEXT CHECK(status IN ('available', 'reserved', 'borrowed', 'damaged')) NOT NULL,
    reservation_count INT DEFAULT 0,
    borrower_id INT
)
''')

cursor.execute('''
CREATE TABLE Reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    book_id INT,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('confirmed', 'cancelled', 'completed', 'failed')) NOT NULL,
    book_location VARCHAR(50) NOT NULL,
    reservation_location VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
)
''')

cursor.execute('''
CREATE TABLE Activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR(100) NOT NULL,
    link VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE Review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    book_id INT,
    content TEXT NOT NULL,
    rating INT CHECK(rating >= 1 AND rating <= 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
)
''')

cursor.execute('''
CREATE TABLE Score (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    points INT NOT NULL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)
''')

# 生成密码哈希
hashed_password = generate_password_hash('password123')

# 插入不同角色的用户，使用哈希后的密码
cursor.execute('''INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)''',
               ('student_user', hashed_password, 'student@example.com', 'student'))
cursor.execute('''INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)''',
               ('teacher_user', hashed_password, 'teacher@example.com', 'teacher'))
cursor.execute('''INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)''',
               ('admin_user', hashed_password, 'admin@example.com', 'admin'))


book_pth = 'app/utils/books/book_information.txt'
f = open(book_pth, 'r', encoding='utf-8')
lines = f.readlines()

for i in range(0, len(lines), 9):
    title = lines[i].split(' ')[2].strip()
    book_image = lines[i+1].split(' ')[2].strip()
    book_image = open(book_image, 'rb').read()
    author = lines[i+2].split(' ')[2].strip()
    publisher = lines[i+3].split(' ')[2].strip()
    publish_date = lines[i+4].split(' ')[2].strip()
    isbn = lines[i+5].split(' ')[2].strip()
    status = lines[i+6].split(' ')[2].strip()
    location = lines[i+7].split(' ')[2].strip()
    cursor.execute('INSERT INTO Book(title, book_image, author, publisher, publish_date, isbn, status, location) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (title, book_image, author, publisher, publish_date, isbn, status, location))
    conn.commit()

# 提交事务
conn.commit()

# 关闭数据库连接
conn.close()

# 测试数据库创建

conn = sqlite3.connect('database_test.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    points INT DEFAULT 0,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT CHECK(role IN ('student', 'teacher', 'admin')) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE Book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    book_image BLOB,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    publish_date DATE NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    location VARCHAR(50) NOT NULL,
    status TEXT CHECK(status IN ('available', 'reserved', 'borrowed', 'damaged')) NOT NULL,
    reservation_count INT DEFAULT 0,
    borrower_id INT
)
''')

cursor.execute('''
CREATE TABLE Reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    book_id INT,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('confirmed', 'cancelled', 'completed', 'failed')) NOT NULL,
    book_location VARCHAR(50) NOT NULL,
    reservation_location VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
)
''')

cursor.execute('''
CREATE TABLE Activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR(100) NOT NULL,
    link VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE Review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    book_id INT,
    content TEXT NOT NULL,
    rating INT CHECK(rating >= 1 AND rating <= 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
)
''')

cursor.execute('''
CREATE TABLE Score (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    points INT NOT NULL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)
''')

# 提交事务
conn.commit()

# 关闭数据库连接
conn.close()

print("数据库初始化完成，数据已插入。")
