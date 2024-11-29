import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

# Тестовая конфигурация тестирования веток
logging.basicConfig(level=logging.INFO)
TOKEN = "8027892189:AAH2_7dXqJWNLC4i7ZlySE0vsexuYWmygYU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

data_file = 'data.json'


# Функция для чтения данных из JSON-файла
def read_data():
    if not os.path.exists(data_file):
        return {'users': [], 'products': [], 'messages': [], 'orders': []}
    with open(data_file, 'r') as f:
        return json.load(f)


# Функция для записи данных в JSON-файл
def write_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)


@dp.message(Command("starti"))
async def start(message: types.Message):
    await message.reply("Здравствуйте")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть заказы", callback_data="view_orders")],
        [InlineKeyboardButton(text="Добавить товар", callback_data="add_product")],
        [InlineKeyboardButton(text="Удалить товар", callback_data="remove_product")]
    ])
    await message.reply("Вы можете посмотреть заказы, добавить или удалить товар, нажав на кнопку ниже:", reply_markup=keyboard)


@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "view_orders":
        data = read_data()

        # Получаем все заказы
        all_orders = data.get('orders', [])

        if not all_orders:
            await bot.send_message(callback.from_user.id, "Нет доступных заказов.")
        else:
            orders_message = "Все заказы:\n"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_help")]
            ])

            for index, order in enumerate(all_orders):
                order_id = order.get('id', index)
                order_text = f"Пользователь: {order['username']}, Заказ: {order['items']}, Общая сумма: {order['total']}"
                orders_message += f"{order_text}\n"

            await bot.send_message(callback.from_user.id, orders_message, reply_markup=keyboard)

    elif callback.data == "add_product":
        await bot.send_message(callback.from_user.id, "Пожалуйста, введите название товара, цену и ссылку на изображение в формате: название, цена, ссылка")

    elif callback.data == "remove_product":
        data = read_data()
        products = data.get('products', [])
        if not products:
            await bot.send_message(callback.from_user.id, "Нет доступных товаров для удаления.")
            return

        products_list = "\n".join([f"{index + 1}. {product['name']}" for index, product in enumerate(products)])
        await bot.send_message(callback.from_user.id, f"Доступные товары для удаления:\n{products_list}\n\nВведите номер товара для удаления.")

    elif callback.data == "back_to_help":
        await help_command(callback.message)

@dp.message()
async def echo(message: types.Message):
    if ',' in message.text:
        try:
            product_name, product_price, product_image_url = [part.strip() for part in message.text.split(',', 2)]
            product_price = float(product_price)  # Преобразуем цену в число
            data = read_data()
            new_product = {
                'name': product_name,
                'price': product_price,
                'image_path': product_image_url
            }
            data['products'].append(new_product)
            write_data(data)
            await message.reply(f"Товар '{product_name}' добавлен с ценой {product_price} и изображением по ссылке {product_image_url}.")
        except ValueError:
            await message.reply("Ошибка: убедитесь, что цена является числом.")
    else:
        # Проверка на удаление товара
        data = read_data()
        products = data.get('products', [])
        try:
            product_index = int(message.text) - 1  # Преобразуем текст в индекс
            if 0 <= product_index < len(products):
                removed_product = products.pop(product_index)
                write_data(data)
                await message.reply(f"Товар '{removed_product['name']}' удален.")
            else:
                await message.reply("Ошибка: неверный номер товара. Пожалуйста, введите корректный номер.")
        except ValueError:
            await message.reply("Ошибка: введите номер товара для удаления.")

async def start_db():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_db())