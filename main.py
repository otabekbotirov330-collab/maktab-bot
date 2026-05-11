import os
from aiohttp import web # Kichik web server uchun

# ... (oldingi kodlaringiz: TOKEN, ADMIN_ID va h.k.)

# Render uchun maxsus: Bot o'chib qolmasligi uchun port ochamiz
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def main():
    # Web serverni bot bilan birga ishga tushiramiz
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAE0i-8p4A777M9zq70IxhTl2DE4-8VzV8Y" # @BotFather'dan olingan kod
ADMIN_ID = 8323916383 # O'zingizning ID raqamingiz (@userinfobot orqali bilish mumkin)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HOLATLAR (FSM) ---
class Form(StatesGroup):
    ism = State()
    mavzu = State()
    tavsif = State()

# --- START BUYRUG'I ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Maktab ma'muriyati o'quvchilar tashabbuslarini doim qo'llab-quvvatlaydi.\n\n"
        "Yangi tashabbus yuborish uchun /tashabbus buyrug'ini bosing."
    )

# --- ANKETA BOSHLASH ---
@dp.message(Command("tashabbus"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Ismingiz va sinfingizni yozing:")
    await state.set_state(Form.ism)

@dp.message(Form.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Tashabbusingizning mavzusi nima? (Masalan: Robototexnika to'garagi)")
    await state.set_state(Form.mavzu)

@dp.message(Form.mavzu)
async def get_topic(message: types.Message, state: FSMContext):
    await state.update_data(mavzu=message.text)
    await message.answer("Tashabbusingiz haqida batafsil ma'lumot bering (Nega bu muhim?):")
    await state.set_state(Form.tavsif)

@dp.message(Form.tavsif)
async def get_desc(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    tavsif = message.text
    
    # Maslahatchiga (Admin) xabar yuborish
    report_text = (
        f"?? Yangi tashabbus kelib tushdi!\n\n"
        f"?? Kimdan: {user_data['ism']}\n"
        f"?? Mavzu: {user_data['mavzu']}\n"
        f"?? Batafsil: {tavsif}\n"
        f"?? User: @{message.from_user.username}"
    )
    
    await bot.send_message(ADMIN_ID, report_text)
    await message.answer("Rahmat! Sizning arizangiz maktab maslahatchisiga yuborildi. Tez orada javob olasiz.")
    await state.clear()

# --- BOTNI ISHGA TUSHIRISH ---
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
import os
from aiohttp import web # Kichik web server uchun

# ... (oldingi kodlaringiz: TOKEN, ADMIN_ID va h.k.)

# Render uchun maxsus: Bot o'chib qolmasligi uchun port ochamiz
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def main():
    # Web serverni bot bilan birga ishga tushiramiz
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())