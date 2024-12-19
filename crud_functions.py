import sqlite3
import string
import re
#  Если не открывать и закрывать базу в каждой функции, то при повторном выборе товаров по кнопке
# "Купить" и "Регистрация" вылетает ошибка о том что база закрыта


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    prod = cursor.execute("SELECT id FROM Products WHERE id = 1")
    # Если нет продукции с id = 1, то заполняем таблицу значениями
    if prod.fetchone() is None:
        for i in range(1, 5):
            cursor.execute("INSERT INTO Products (title,description,price) VALUES (?,?,?)",
                           (f'Продукт {i}', f'Описание {i}', i * 100))

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    prod_all = cursor.fetchall()
    # Закроем базу
    connection.close()
    return prod_all


def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    user = cursor.execute("SELECT username FROM Users WHERE username = ?",(username,))
    if user.fetchone() is None:
        return True
    else:
        return False

def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username,email,age,balance) VALUES (?,?,?,?)",
                   (username,email,age,1000))
    connection.commit()
    connection.close()

# Проверка username на правильность заполнения
def latin_string(input_string):
    if all(c in string.ascii_letters for c in input_string):
        return True
    return False

# Проверка email на правильность заполнения
def email_valid_address(email):
    pattern = re.compile(r"^\S+@\S+\.\S+$")
    valid = pattern.match(email)
    if valid:
        return True
    else:
        return False

