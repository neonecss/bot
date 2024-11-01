import sqlite3
import time
import random
from collections import Counter

# Подключение к базе данных
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

boxes = {
    1: {"classification": ""},
    2: {"classification": ""},
    3: {"classification": ""},
}

# Функция, которая будет обращаться к другому файлу (сканирование QR и return полученного значения)
def scanQR():
    result = random.randint(1, 3)  # Генерирует число от 1 до 3, симулируя работу сканирования и получения ID item
    return result

# Функция сборки заказа
def assemblyOrder():
    # Бесконечный цикл для проверки наличия новых записей
    while True:
        cursor.execute("SELECT items FROM orders")  # Выбираем все items из orders
        rows = cursor.fetchall()  # Подтверждаем
        if rows:  # Если есть новые значения
            for (message,) in rows:  # Перебираем, убирая все ненужные знаки
                itemsSplited = message.split(':')  # Разделяем items через :
                # Подсчет количества каждого item
                item_counts = Counter(itemsSplited)         
                for item in item_counts:  # Цикл перебора items
                    item_num = int(item)
                    quantity = item_counts[item]  # Количество для текущего item
                    print(f"Processing {item} with quantity {quantity}")

                    # Сравнение и вывод принадлежности для каждого количества
                    for _ in range(quantity):  # Цикл для количества
                        found = False  # Флаг для отслеживания, найдено ли совпадение
                        for index, box in boxes.items():
                            # Сравнение с преобразованием classification в число
                            if box["classification"] and int(box["classification"]) == item_num:
                                print(f"Item {item} принадлежит индексу {index}")
                                found = True
                                break
                        if not found:
                            print(f"Item {item} не найден в классификациях boxes")
        break

# Функция запускаемая самой первой, для сканирования QR и записи значений в словарь boxes
def start():
    i = 0  # Переменная итераций цикла
    # Цикл, где 3 - количество коробок, когда мы просмотрим все 3 коробки выполнение завершится
    while i < 3:  # Изменено условие на < 3 для корректной работы
        i += 1  # +1 к итерациям
        print(i)
        time.sleep(2)
        scanResult = scanQR()
        boxes[i]["classification"] = scanResult  # Случайное значение от 1 до 3
        print(boxes)
    assemblyOrder()

start()
