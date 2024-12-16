import sqlite3
#  Если не открывать и закрывать базу в каждой функции, то при повторном выборе товаров по кнопке
# "Купить" вылетает ошибка о том что база закрыта

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
