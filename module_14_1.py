# Создание БД, добавление, выбор и удаление элементов.
import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username,email,age,balance) VALUES (?,?,?,?)",
                   (f'User{i}', f'example{i}@gmail.com', str(i * 10), str(1000)))

cursor.execute("UPDATE Users SET balance = ? WHERE id % 2 = ?", (str(500), not 0))
cursor.execute("DELETE FROM Users where id%3 = 1")
cursor.execute("SELECT username,email,age,balance  FROM Users where age != 60")
users = cursor.fetchall()

#
for i in users:
    #    print(*list(i), sep='|')
    print(f'Имя: {list(i)[0]}|Почта: {list(i)[1]}|Возраст: {list(i)[2]}|Баланс: {list(i)[3]}')

connection.commit()
connection.close()
