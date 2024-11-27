import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging

bot = Bot("7605960349:AAECPUTKkAm_8RR1wvWWMQKYYv8OS8AgQ2Y")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Список матерных слов
bad_words = [
    "сука", "блядь", "хуй", "пизда", "ебать", "мудила", "долбоеб", "урод", "козел", "гандон", "блять", "гнида"
    # Добавьте сюда другие матерные слова по вашему усмотрению
]

@dp.message(Command('delete'))
async def delete_message(msg: types.Message):
    if msg.reply_to_message:
        message_id_to_delete = msg.reply_to_message.message_id
        chat_id = msg.chat.id

        await bot.delete_message(chat_id, message_id_to_delete)
        await msg.answer("Сообщение удалено.")
    else:
        await msg.answer("Пожалуйста, ответьте на сообщение, которое хотите удалить.")

@dp.message()
async def auto_delete_message(msg: types.Message):
    # Проверяем, содержит ли сообщение любое из матерных слов
    if any(bad_word in msg.text.lower() for bad_word in bad_words):
        await bot.delete_message(msg.chat.id, msg.message_id)  # Удаляем сообщение
        logging.info(f"Удалено сообщение: {msg.text}")  # Логируем удаление сообщения

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())