import sqlite3

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

cursor.execute("""
    create table Book(
        book_id char(8) primary key,
        book_name char(100),
        book_image blob,
        book_author char(100),
        book_location char(100),
        book_score float,
        book_storage char(50),
        book_reservation_time float,
        book_reservation_location char(100)
    )
""")

cursor.execute("""
    create table StudentAccount(
        net_id char(8) primary key,
        name char(100),
        gain int,
        password char(100)
    )
    """)

cursor.execute("""
    create table TeacherAccount(
        net_id char(8) primary key,
        name char(100),
        real_name char(100),
        gain int,
        password char(100)
    )
""")

cursor.execute("""
    create table AdminAccount(
        net_id char(8) primary key,
        name char(100),
        gain int,
        real_name char(100),
        password char(100)
    )
""")

cursor.execute("""
    create table Comment(
        net_id char(8),
        book_id char(8),
        comment char(1000),
        score int,
        time float,
        primary key(net_id, book_id)
    )
""")

cursor.execute("""
    create table ReservationBook(
        net_id char(8),
        book_id char(8),
        time float,
        primary key(net_id, book_id)
    )
""")

cursor.execute("""
    create table BorrowBook(
        net_id char(8),
        book_id char(8),
        time float,
        primary key(net_id, book_id)
    )
""")
