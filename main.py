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
TOKEN = "TOKEN_YERI" # O'z tokeningizni qo'ying
ADMIN_ID = 8323916383 
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

# --- 50 TA PROFESSIONAL SAVOL ---
# Bu savollar o'quvchining qiziqishlarini aniqlashga yordam beradi
QUESTIONS = [
    "1. Kompyuter dasturlari qanday ishlashiga qiziqasizmi?",
    "2. Tabiat va ekologiyani asrash siz uchun muhimmi?",
    "3. Robotlarni yasash yoki boshqarishni xohlaysizmi?",
    "4. Matematik masalalarni yechish sizga zavq beradimi?",
    "5. Kelajakda sun'iy intellekt bilan ishlashni xohlaysizmi?",
    "6. Odamlarga psixologik yordam berish sizga yoqadimi?",
    "7. Yangi texnologik qurilmalarni qismlarga ajratib ko'rasizmi?",
    "8. Videomontaj yoki rasm tahrirlashga qiziqasizmi?",
    "9. Chet tillarini o'rganish siz uchun osonmi?",
    "10. Jamoada yetakchi (lider) bo'lishni yoqtirasizmi?",
    "11. Tibbiyot va inson salomatligi sohasida ishlashni xohlaysizmi?",
    "12. Kosmos va astronomiya sizni o'ziga tortadimi?",
    "13. Kimyoviy tajribalar o'tkazishga qiziqasizmi?",
    "14. Iqtisodiyot va biznes yuritishni o'rganmoqchimisiz?",
    "15. Arxitektura va binolar loyihasini chizish yoqadimi?",
    "16. Qishloq xo'jaligida innovatsiyalarni qo'llashga qiziqasizmi?",
    "17. Huquqshunos bo'lib odamlar haqini himoya qilishni xohlaysizmi?",
    "18. Avtomobillar dvigateli va tuzilishi sizga qiziqmi?",
    "19. Jurnalistika yoki blogerlik sohasiga qiziqasizmi?",
    "20. Sport bilan professional shug'ullanishni xohlaysizmi?",
    "21. Dizayn va modaga qiziqishingiz bormi?",
    "22. O'qituvchilik qilib bilim ulashish sizga yoqadimi?",
    "23. Kiberxavfsizlik (hakerlardan himoya) sohasiga qiziqasizmi?",
    "24. Chet davlatlarda o'qish va ishlashni maqsad qilganmisiz?",
    "25. Grafik dizayn va animatsiya yaratish sizga qiziqmi?",
    "26. Logistika va transport tizimini boshqarish yoqadimi?",
    "27. Biotexnologiya va gen muhandisligiga qiziqasizmi?",
    "28. Siyosat va davlat boshqaruvi sizga qiziqmi?",
    "29. Xalqaro aloqalar va diplomatiyani yoqtirasizmi?",
    "30. Moliyaviy tahlil va birja bilan ishlashni xohlaysizmi?",
    "31. Qurilish muhandisligi sizga yoqadimi?",
    "32. Turizm va mehmonxona biznesiga qiziqasizmi?",
    "33. Psixologiya va inson xatti-harakatlarini o'rganish yoqadimi?",
    "34. Muhandislik chizmalari bilan ishlashga qiziqasizmi?",
    "35. Sahna san'ati va aktyorlikka qiziqishingiz bormi?",
    "36. Ekologik toza energiya (quyosh, shamol) manbalari qiziqmi?",
    "37. Ma'lumotlar bazasi bilan ishlash yoqadimi?",
    "38. Oziq-ovqat texnologiyasi va yangi mahsulotlar yaratish qiziqmi?",
    "39. Arxeologiya va tarixiy tadqiqotlar sizga yoqadimi?",
    "40. Dengiz yoki aviatsiya sohasida ishlashni xohlaysizmi?",
    "41. Nanotexnologiyalar kelajagiga ishonasizmi?",
    "42. Ijtimoiy tarmoqlar uchun kreativ kontent yaratasizmi?",
    "43. Kitob o'qish va adabiyotga qiziqasizmi?",
    "44. Xayriya ishlari va volontyorlik bilan shug'ullanasizmi?",
    "45. Zamonaviy bank tizimini o'rganish yoqadimi?",
    "46. Videoo'yinlar yaratish (gamedev) sizga qiziqmi?",
    "47. Faylasuflik va mantiqiy fikrlash yoqadimi?",
    "48. Shaharsozlik (Urbanistika) muammolari sizni qiziqtiradimi?",
    "49. Marketing va reklama sohasida ishlashni xohlaysizmi?",
    "50. Kelajakda o'z shaxsiy biznesingizni ochmoqchimisiz?"
]

# --- ASOSIY HANDLERLAR ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Testdan o'tish")
    builder.button(text="ℹ️ Maslahatchi")
    builder.adjust(2)
    await message.answer("Assalomu alaykum! Maktab maslahatchisi botiga xush kelibsiz.", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "📝 Testdan o'tish")
async def quiz_name_ask(message: types.Message, state: FSMContext):
    await message.answer("📝 So'rovnomani boshlash uchun Ism va Familiyangizni kiriting:")
    await state.set_state(QuizState.waiting_name)

@dp.message(QuizState.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text, current_q=0, total_score=0)
    builder = InlineKeyboardBuilder().button(text="🚀 Boshlash", callback_data="start_quiz")
    await message.answer(f"Rahmat, {message.text}! Savollar tayyor. Boshlaymizmi?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "start_quiz")
async def run_quiz(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="q_1").button(text="❌ Yo'q", callback_data="q_0")
    await callback.message.edit_text(f"1-savol: {QUESTIONS[0]}", reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def handle_quiz_steps(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr = data['current_q']
    score = data['total_score'] + int(callback.data.split("_")[1])
    
    curr += 1
    if curr < len(QUESTIONS):
        await state.update_data(current_q=curr, total_score=score)
        builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="q_1").button(text="❌ Yo'q", callback_data="q_0")
        await callback.message.edit_text(f"{curr+1}-savol: {QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        full_name = data['full_name']
        await state.clear()
        
        # Sertifikat yaratish (oddiyroq usulda)
        img = Image.new('RGB', (800, 600), color=(0, 102, 204))
        d = ImageDraw.Draw(img)
        d.rectangle([20, 20, 780, 580], fill=(255, 255, 255))
        d.text((400, 150), "SERTIFIKAT", fill=(0, 102, 204), anchor="mm")
        d.text((400, 300), full_name, fill=(0, 0, 0), anchor="mm")
        d.text((400, 450), f"Ball: {score}/50", fill=(204, 0, 0), anchor="mm")
        
        cert_path = os.path.join(CERT_FOLDER, f"res_{callback.from_user.id}.png")
        img.save(cert_path)
        
        await callback.message.delete()
        await bot.send_photo(callback.from_user.id, photo=FSInputFile(cert_path), caption="🏁 Tabriklaymiz! Test yakunlandi.")
        await bot.send_message(ADMIN_ID, f"📊 Yangi natija: {full_name} - {score} ball")
    
    await callback.answer()

async def main():
    # Render uchun portni band qilish
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
