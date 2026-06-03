import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAE0i-8p4A777M9zq70IxhTl2DE4-8VzV8Y"[cite: 1]
ADMIN_ID = 8323916383[cite: 1]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HOLATLAR (FSM) ---
class Form(StatesGroup):
    ism = State()[cite: 1]
    mavzu = State()[cite: 1]
    tavsif = State()[cite: 1]
    tasdiqlash = State()

# --- TUGMALAR ---
def bekor_qilish_tugmasi():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)

def tasdiqlash_tugmalari():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="✅ Yuborish"))
    builder.add(types.KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)

# --- BEKOR QILISH HANDLERI ---
@dp.message(F.text == "❌ Bekor qilish")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Jarayon bekor qilindi.", reply_markup=types.ReplyKeyboardRemove())

# --- START BUYRUG'I ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Maktab ma'muriyati o'quvchilar tashabbuslarini doim qo'llab-quvvatlaydi.\n\n"
        "Yangi tashabbus yuborish uchun /tashabbus buyrug'ini bosing.",
        reply_markup=types.ReplyKeyboardRemove()
    )[cite: 1]

# --- ANKETA BOSHLASH ---
@dp.message(Command("tashabbus"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Ismingiz va sinfingizni yozing:", reply_markup=bekor_qilish_tugmasi())[cite: 1]
    await state.set_state(Form.ism)[cite: 1]

@dp.message(Form.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)[cite: 1]
    await message.answer("Tashabbusingizning mavzusi nima?", reply_markup=bekor_qilish_tugmasi())[cite: 1]
    await state.set_state(Form.mavzu)[cite: 1]

@dp.message(Form.mavzu)
async def get_topic(message: types.Message, state: FSMContext):
    await state.update_data(mavzu=message.text)[cite: 1]
    await message.answer("Tashabbusingiz haqida batafsil ma'lumot bering:", reply_markup=bekor_qilish_tugmasi())[cite: 1]
    await state.set_state(Form.tavsif)[cite: 1]

@dp.message(Form.tavsif)
async def get_desc(message: types.Message, state: FSMContext):
    await state.update_data(tavsif=message.text)
    user_data = await state.get_data()
    
    preview = (
        f"📋 **Ma'lumotlaringizni tekshiring:**\n\n"
        f"👤 Kimdan: {user_data['ism']}\n"
        f"📌 Mavzu: {user_data['mavzu']}\n"
        f"📝 Batafsil: {user_data['tavsif']}\n\n"
        f"Hamma ma'lumotlar to'g'rimi?"
    )
    await message.answer(preview, reply_markup=tasdiqlash_tugmalari(), parse_mode="Markdown")
    await state.set_state(Form.tasdiqlash)

@dp.message(Form.tasdiqlash, F.text == "✅ Yuborish")
async def send_report(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    
    report_text = (
        f"🚀 **Yangi tashabbus!**\n\n"
        f"👤 **Kimdan:** {user_data['ism']}\n"
        f"📌 **Mavzu:** {user_data['mavzu']}\n"
        f"📝 **Batafsil:** {user_data['tavsif']}\n"
        f"🔗 **User:** {username}\n"
        f"🆔 **ID:** `{message.from_user.id}`"
    )
    
    await bot.send_message(ADMIN_ID, report_text, parse_mode="Markdown")[cite: 1]
    await message.answer("Rahmat! Sizning arizangiz yuborildi.", reply_markup=types.ReplyKeyboardRemove())[cite: 1]
    await state.clear()[cite: 1]

# --- BOTNI ISHGA TUSHIRISH ---
async def main():
    print("Bot ishga tushdi...")[cite: 1]
    await dp.start_polling(bot)[cite: 1]

if __name__ == "__main__":
    try:
        asyncio.run(main())[cite: 1]
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")[cite: 1]
