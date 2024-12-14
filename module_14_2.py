# Выбор элементов и функции в SQL запросах
import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
# Удаляем строку с id = 6
cursor.execute("DELETE FROM Users where id = ?", (6,))
# Подсчитаем общее количество записей.
cursor.execute("SELECT COUNT() FROM Users")
total_users = cursor.fetchone()[0]
# Подсчитаем сумму всех балансов
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]
# Подсчитаем среднее
print(all_balances / total_users)

connection.commit()
connection.close()
