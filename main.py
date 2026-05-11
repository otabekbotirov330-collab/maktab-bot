import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAE0i-8p4A777M9zq70IxhTl2DE4-8VzV8Y"
ADMIN_ID = 5484803761 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- WEB SERVER (Render uchun) ---
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

# --- BOT LOGIKASI ---
class Form(StatesGroup):
    ism = State()
    mavzu = State()
    tavsif = State()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Maktab maslahatchisi botiga xush kelibsiz. Tashabbus yuborish uchun /tashabbus buyrug'ini bosing.")

@dp.message(Command("tashabbus"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Ismingiz va sinfingizni yozing:")
    await state.set_state(Form.ism)

@dp.message(Form.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Tashabbusingiz mavzusi nima?")
    await state.set_state(Form.mavzu)

@dp.message(Form.mavzu)
async def get_topic(message: types.Message, state: FSMContext):
    await state.update_data(mavzu=message.text)
    await message.answer("Tashabbus haqida batafsil ma'lumot bering:")
    await state.set_state(Form.tavsif)

@dp.message(Form.tavsif)
async def get_desc(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    report = (f"📩 YANGI TASHABBUS!\n\n👤 Kimdan: {user_data['ism']}\n"
              f"📌 Mavzu: {user_data['mavzu']}\n📝 Tavsif: {message.text}")
    
    try:
        await bot.send_message(ADMIN_ID, report)
        await message.answer("Rahmat! Tashabbusingiz qabul qilindi va maslahatchiga yuborildi.")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Keyinroq qayta urinib ko'ring.")
        logging.error(f"Xabar yuborishda xatolik: {e}")
    
    await state.clear()

async def main():
    # Web serverni sozlash
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
