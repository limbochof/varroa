import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.filters import Command

# Получение токена из переменных окружения
TOKEN = os.getenv("TOKEN")

# Команды, кто может открывать
GATE_RESPONDERS = ["MadiyarYntykbay", "Tinbrawl", "limbachof"]
OPEN_RESPONDERS = ["KhanWarden", "teemudzhinn", "Garmaevvlad", "danayergali"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда: открытие ворот
@dp.message(Command("gate"))
async def request_gate(message: Message):
    requester = message.from_user.username or message.from_user.full_name
    gate_location = "с Айтиева"
    tagged_users = " ".join([f"@{u}" for u in GATE_RESPONDERS])
    text = f"🔐 Запрос на открытие ворот {gate_location} от @{requester}.

{tagged_users}

"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Не Открыто", callback_data="gate_opened")]
    ])
    await message.answer(text, reply_markup=keyboard)

# Команда: открытие шлагбаума
@dp.message(Command("open"))
async def request_barrier(message: Message):
    requester = message.from_user.username or message.from_user.full_name
    tagged_users = " ".join([f"@{u}" for u in OPEN_RESPONDERS])
    text = f"🛡 Запрос на открытие шлагбаума от @{requester}.

{tagged_users}

"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Не Открыто", callback_data="barrier_opened")]
    ])
    await message.answer(text, reply_markup=keyboard)

# Обработка кнопки "Открыто" — ворота
@dp.callback_query(lambda c: c.data == "gate_opened")
async def handle_gate_opened(callback: types.CallbackQuery):
    opener = callback.from_user.username or callback.from_user.full_name
    if opener not in GATE_RESPONDERS:
        await callback.answer("⛔ У вас нет прав открывать ворота", show_alert=True)
        return
    new_text = callback.message.text.replace("❌ Пока не открыто", f"✅ Открыл @{opener}")
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Готово!")

# Обработка кнопки "Открыто" — шлагбаум
@dp.callback_query(lambda c: c.data == "barrier_opened")
async def handle_barrier_opened(callback: types.CallbackQuery):
    opener = callback.from_user.username or callback.from_user.full_name
    if opener not in OPEN_RESPONDERS:
        await callback.answer("⛔ У вас нет прав открывать шлагбаум", show_alert=True)
        return
    new_text = callback.message.text.replace("❌ Пока не открыто", f"✅ Открыл @{opener}")
    await callback.message.edit_text(new_text, reply_markup=None)
    await callback.answer("Готово!")

# Команды
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="open", description="🛡 Запрос на открытие шлагбаума"),
        BotCommand(command="gate", description="🚪 Запрос на открытие ворот с Айтиева"),
    ]
    await bot.set_my_commands(commands)

# Запуск
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
