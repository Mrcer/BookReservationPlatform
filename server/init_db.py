import sqlite3

conn = sqlite3.connect('database.sqlite')
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