import telebot
from telebot import types
import sqlite3

# Подключаем бота
API_TOKEN = '7242408868:AAH1BWwck2KKJqPhHGZSwp2F0-Uq0xTC9h0'
bot = telebot.TeleBot(API_TOKEN)

# Создаем базу данных, если её нет
with sqlite3.connect("orders.db") as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orders(order_id INTEGER PRIMARY KEY, items TEXT, status INTEGER DEFAULT 1)")

# Данные о товарах и корзине
cart = {}
items = {
    1: {"name": "item 1"},
    2: {"name": "item 2"},
    3: {"name": "item 3"},
}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for item_id, info in items.items():
        button = types.InlineKeyboardButton(f"{info['name']}", callback_data=f"add_{item_id}")
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите товар для добавления в корзину:", reply_markup=markup)

# Обработчик для добавления товаров в корзину
@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart(call):
    user_id = call.from_user.id
    product_id = int(call.data.split("_")[1])

    # Создаем корзину пользователя, если её еще нет
    if user_id not in cart:
        cart[user_id] = []

    # Добавляем товар в корзину
    cart[user_id].append(items[product_id])
    bot.answer_callback_query(call.id, f"Добавлено: {items[product_id]['name']}")

# Команда для отображения корзины
@bot.message_handler(commands=["cart"])
def show_cart(message):
    user_id = message.from_user.id
    if user_id not in cart or not cart[user_id]:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return

    # Отображение товаров в корзине
    cart_text = "Ваша корзина:\n" + '\n'.join(item['name'] for item in cart[user_id])
    
    # Кнопка для оформления заказа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Оформить заказ"))
    bot.send_message(message.chat.id, cart_text, reply_markup=markup)

# Команда для очистки корзины
@bot.message_handler(commands=["clear_cart"])
def clear_cart(message):
    user_id = message.from_user.id
    cart[user_id] = []
    bot.send_message(message.chat.id, "Ваша корзина очищена.")

# Оформление заказа
@bot.message_handler(func=lambda message: message.text == "Оформить заказ")
def create_order(message):
    user_id = message.from_user.id
    if user_id not in cart or not cart[user_id]:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return

    # Преобразуем список товаров в строку
    order_items = ':'.join(item['name'] for item in cart[user_id])

    # Подключение к базе данных и сохранение заказа
    with sqlite3.connect("orders.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders (items, status) VALUES (?, ?)", (order_items, 1))  # 1 - статус "новый заказ"
        con.commit()  # Подтверждаем изменения в базе данных

    bot.send_message(message.chat.id, "Ваш заказ оформлен!")
    cart[user_id] = []  # Очищаем корзину после заказа

if __name__ == '__main__':
    bot.polling(none_stop=True)
