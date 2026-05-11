import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAELPbVp4gM2ZkJrHGtCoWyfpWIbY3_lB0Y"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HOLATLAR (States) ---
class AdvisorForm(StatesGroup):
    yonalish = State()
    ism = State()
    savol = State()

# --- WEB SERVER ---
async def handle(request):
    return web.Response(text="Maslahatchi boti faol!")

# --- TUGMALAR ---
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎯 Kasbga yo'naltirish")
    builder.button(text="🧠 Psixologik maslahat")
    builder.button(text="💡 Taklif va tashabbuslar")
    builder.button(text="❓ Umumiy savollar")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- BOT LOGIKASI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        "Men — Maktab maslahatchisi botiman. Sizga qanday yordam bera olaman?",
        reply_markup=get_main_menu()
    )

@dp.message(F.text.in_(["🎯 Kasbga yo'naltirish", "🧠 Psixologik maslahat", "💡 Taklif va tashabbuslar", "❓ Umumiy savollar"]))
async def select_category(message: types.Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer("To'liq ismingiz va sinfingizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdvisorForm.ism)

@dp.message(AdvisorForm.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    data = await state.get_data()
    await message.answer(f"Tushunarli. Endi '{data['yonalish']}' bo'yicha murojaatingizni batafsil yozib qoldiring:")
    await state.set_state(AdvisorForm.savol)

@dp.message(AdvisorForm.savol)
async def get_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    report = (
        f"📩 **YANGI MUROJAAT!**\n\n"
        f"📂 **Yo'nalish:** {user_data['yonalish']}\n"
        f"👤 **Kimdan:** {user_data['ism']}\n"
        f"📝 **Murojaat:** {message.text}\n"
        f"🔗 **Username:** @{message.from_user.username or 'mavjud emas'}"
    )
    
    try:
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        await message.answer("Rahmat! Murojaatingiz maslahatchiga yuborildi. Tez orada siz bilan bog'lanishadi.", reply_markup=get_main_menu())
    except Exception as e:
        await message.answer("Xatolik! Adminga xabar yuborib bo'lmadi.", reply_markup=get_main_menu())
    
    await state.clear()

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
