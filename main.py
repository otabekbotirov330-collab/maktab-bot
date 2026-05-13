import os
import asyncio
import logging
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAEj9P..." # Bot tokeningiz
ADMIN_ID = 8323916383 # Sizning ID raqamingiz
ADMIN_FOLDER = "admin_data"
CERT_FOLDER = "certificates"

for folder in [ADMIN_FOLDER, CERT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class QuizState(StatesGroup):
    waiting_name = State()
    answering = State()

# --- SAVOLLAR VA MA'LUMOTLAR ---
QUESTIONS = [f"{i}-savol. Tanlagan yo'nalishingiz bo'yicha mustaqil loyihalar qilish sizga yoqadimi?" for i in range(1, 51)]

CAREER_TIPS = [f"{i}. " + t for i, t in enumerate([
    "IKIGAI metodini o'rganing.", "Mehnat bozorini tahlil qiling.", "IT sohasini chetlab o'tmang.",
    "Xorijiy tillar - bu kalit.", "Yumshoq ko'nikmalarni rivojlantiring.", "Mentor toping.",
    "Stajirovkalarga boring.", "Shaxsiy portfolio yarating.", "Sohaviy tadbirlarda qatnashing.",
    "Tanqidiy fikrlashni o'stiring.", "Vaqtni boshqarishni o'rganing.", "Networking qiling.",
    "Kreativlikni oshiring.", "Sun'iy intellektdan foydalaning.", "O'z loyihangizni boshlang.",
    "Kasbiy testlardan o'ting.", "Psixolog maslahatini oling.", "Dunyo trendlarini kuzating.",
    "O'qishdan to'xtamang.", "Sog'liqni saqlang.", "Maqsadni SMART bo'yicha qo'ying.",
    "Xatodan qo'rqmang.", "Tadbirkorlikni o'rganing.", "SMM ko'nikmalarini oling.",
    "Ma'lumotlar tahlilini o'rganing.", "Ekologik kasblarni ko'ring.", "Masofaviy ishlashni sinang.",
    "Shaxsiy brend yarating.", "Jamoada ishlashni o'rganing.", "Nutq mahoratini oshiring.",
    "Liderlikni rivojlantiring.", "Dizayn asoslarini biling.", "Mobil ilovalar yarating.",
    "Kiberxavfsizlikka qiziqing.", "Bulutli texnologiyalarni biling.", "Kitob o'qing.",
    "Podkastlarni tinglang.", "Onlayn kurslarda o'qing.", "Ekspert bo'ling.",
    "Xatolar ustida ishlang.", "Sayohat qiling.", "Yangi madaniyatlarni o'rganing.",
    "Hobbini kasbga aylantiring.", "Daromadni rejalashtiring.", "Investitsiyani o'rganing.",
    "EQni oshiring.", "Robototexnikaga qiziqing.", "Bio-texnologiyalarni ko'ring.",
    "Blockchainni o'rganing.", "Doim izlanishda bo'ling."
], 1)]

# --- SERTIFIKAT VA EXCEL FUNKSIYALARI ---
def create_certificate(full_name, score):
    img = Image.new('RGB', (1000, 700), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 980, 680], outline=(0, 102, 204), width=15)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = font_big = ImageFont.load_default()
    draw.text((500, 150), "SERTIFIKAT", fill=(0, 102, 204), font=font_big, anchor="mm")
    draw.text((500, 350), full_name.upper(), fill=(204, 0, 0), font=font, anchor="mm")
    draw.text((500, 500), f"Natija: {score}/50 ball", fill=(0, 0, 0), font=font, anchor="mm")
    path = os.path.join(CERT_FOLDER, f"cert_{datetime.now().timestamp()}.png")
    img.save(path)
    return path

def update_database(full_name, user_id, score):
    path = os.path.join(ADMIN_FOLDER, "umumiy_natijalar.xlsx")
    df_new = pd.DataFrame({"Sana": [datetime.now().strftime("%d.%m %H:%M")], "F.I.SH": [full_name], "ID": [user_id], "Ball": [score]})
    if os.path.exists(path):
        df_old = pd.read_excel(path)
        df_new = pd.concat([df_old, df_new], ignore_index=True)
    df_new.to_excel(path, index=False)
    return path

# --- ASOSIY MENYU ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Maktab maslahatchisi botiga xush kelibsiz.", reply_markup=main_menu())

@dp.message(F.text == "🔍 Kasb tanlash")
async def career(message: types.Message):
    await message.answer("🎯 **Kasb tanlash bo'yicha 50 ta maslahat:**\n\n" + "\n".join(CAREER_TIPS))

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents(message: types.Message):
    await message.answer("👨‍👩‍👧‍👦 Farzandingiz kelajagiga befarq bo'lmaganingiz uchun rahmat! \n\n1. Uni eshiting.\n2. Qiziqishini qo'llab-quvvatlang.\n3. Majburlamang.")

@dp.message(F.text == "ℹ️ Maslahatchi haqida")
async def about(message: types.Message):
    info = "👤 **Otabek Bakhtiyorovich Botirov**\n🏫 Maktab maslahatchisi\n📍 Farg'ona, Rishton"
    await message.answer(info)

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_start(message: types.Message, state: FSMContext):
    await message.answer("📝 So'rovnomani boshlash uchun Ism va Familiyangizni kiriting:")
    await state.set_state(QuizState.waiting_name)

@dp.message(QuizState.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text, current_q=0, total_score=0)
    builder = InlineKeyboardBuilder().button(text="✅ Boshlash", callback_data="start_quiz")
    await message.answer(f"Rahmat, {message.text}! Tayyormisiz?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "start_quiz")
async def run_quiz(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="q_1").button(text="❌ Yo'q", callback_data="q_0")
    await callback.message.edit_text(f"1-savol: {QUESTIONS[0]}", reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def steps(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data['current_q'], data['total_score'] + int(callback.data.split("_")[1])
    curr += 1
    if curr < len(QUESTIONS):
        await state.update_data(current_q=curr, total_score=score)
        builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="q_1").button(text="❌ Yo'q", callback_data="q_0")
        await callback.message.edit_text(f"Savol {curr+1}/50: {QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        full_name = data['full_name']
        await state.clear()
        db = update_database(full_name, callback.from_user.id, score)
        cert = create_certificate(full_name, score)
        await callback.message.delete()
        await bot.send_photo(callback.from_user.id, photo=FSInputFile(cert), caption=f"🏁 Tabriklaymiz! Ball: {score}/50")
        # Adminga hisobot
        await bot.send_message(ADMIN_ID, f"📊 Yangi natija: {full_name} ({score})")
        await bot.send_document(ADMIN_ID, document=FSInputFile(db))
    await callback.answer()

async def main():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
