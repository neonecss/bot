import sqlite3
import time
from collections import Counter
from picamera2 import Picamera2
from pyzbar.pyzbar import decode, ZBarSymbol
import os

# Уровень логирования для камеры
os.environ["LIBCAMERA_LOG_LEVELS"] = "2"

# Подключение к базе данных
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Инициализация словаря boxes
boxes = {
    1: {"classification": ""},
    2: {"classification": ""},
    3: {"classification": ""},
}

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
                                print(f'Новая итерация с item {item}')
                                print(f"Item {item} принадлежит индексу {index}")
                                found = True
                                break
                        if not found:
                            print(f"Item {item} не найден в классификациях boxes")
        break  # потом вместо break поставить удаление строки из БД

# Функция запускаемая самой первой, для сканирования QR и записи значений в словарь boxes
def start():
    # Внутренняя функция для сканирования QR
    def scanQR():
        start_time = time.time()  # Начало отсчета для 2 секунд ожидания QR
        while time.time() - start_time < 2:  # Проверка в течение 2 секунд
            img = picam2.capture_array()
            decoded = decode(img, symbols=[ZBarSymbol.QRCODE])
            if decoded:
                qr_data = decoded[0].data.decode('utf-8')
                try:
                    return int(qr_data)  # Преобразуем QR-данные в число
                except ValueError:
                    return 0  # Если не число, возвращаем 0
        return 0  # Если за 2 секунды QR-код не найден, вернуть 0

    # Запускаем камеру один раз для использования в цикле
    with Picamera2() as picam2:
        picam2.start()  # Старт камеры
        for i in range(1, 4):  # Перебираем 3 коробки
            print(f"Сканирую коробку {i}")
            time.sleep(2)  # Пауза между сканированиями
            boxes[i]["classification"] = scanQR()  # Записываем результат сканирования
            print(f"Содержимое boxes после сканирования коробки {i}: {boxes}")
        
        assemblyOrder()  # Запуск функции сборки заказа после заполнения boxes

# Запуск основной программы
start()
