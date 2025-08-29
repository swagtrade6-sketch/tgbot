from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8224907422:AAHM8jkdhTHFXrTJDCTcomep8jvZj6hjwGU"
OWNER_ID = 5992958475  # твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Храним пользователей, которые уже отправили запрос
requested_users = set()

# Команда /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="📞 Связаться",
            callback_data="request_contact"
        )
    )
    await message.answer(
        "👋 Чтобы связаться с владельцем, нажмите кнопку ниже:",
        reply_markup=keyboard
    )

# Обработка текста
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def block_text(message: types.Message):
    if message.from_user.id in requested_users:
        await message.reply("⏳ Ожидайте, вы уже отправили запрос на связь.")
    else:
        await message.reply("❌ Писать сюда не нужно.\nНажмите кнопку выше, чтобы отправить запрос.")

# Обработка кнопки
@dp.callback_query_handler(lambda c: c.data == "request_contact")
async def process_request(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    if user.id not in requested_users:
        requested_users.add(user.id)

        # уведомление владельцу
        await bot.send_message(
            OWNER_ID,
            f"📩 Новый запрос на связь!\n"
            f"Пользователь: @{user.username or user.full_name}\n"
            f"ID: {user.id}"
        )
        await callback_query.answer("✅ Запрос отправлен! Ожидайте.")
    else:
        await callback_query.answer("⏳ Вы уже отправили запрос. Ожидайте ответа.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
