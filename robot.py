import sqlite3
import time

# Подключение к базе данных
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Бесконечный цикл для проверки наличия новых записей
while True:
    # Запрашиваем все записи в таблице
    cursor.execute("SELECT items FROM orders")
    rows = cursor.fetchall()
    print(rows)

    # Если найдены записи, выводим их и выходим из цикла
    if rows:
        print("Найдены новые записи:")
        for (message,) in rows:  # Каждая строка - это кортеж, поэтому ставим запятую
            itemsSplited = message.split(':')
        for item in itemsSplited:
            print(item)
        break

    # Ждём 5 секунд перед следующей проверкой
    time.sleep(5)
