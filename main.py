import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAF33A8bsVdAj-_tr66xcVenys8Ls01jsoU"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- TEST SAVOLLARI BAZASI (20 TA) ---
QUESTIONS = [
    "1. Texnik qurilmalarni ta'mirlash sizga yoqadimi?",
    "2. Insonlarga maslahat berishni yoqtirasizmi?",
    "3. Kompyuter dasturlarini o'rganish qiziqarli-mi?",
    "4. Tadbirlar tashkil qilishni yoqtirasizmi?",
    "5. Matematik masalalarni yechish sizga zavq beradimi?",
    "6. Yangi insonlar bilan tanishish siz uchun osonmi?",
    "7. Chizmachilik yoki dizayn bilan shug'ullanasizmi?",
    "8. Laboratoriyada tajribalar o'tkazishni xohlaysizmi?",
    "9. Jamoani boshqarish sizga yoqadimi?",
    "10. Kitob o'qish va tahlil qilishni yoqtirasizmi?",
    "11. Avtomobillar mexanizmiga qiziqasizmi?",
    "12. Kasallarga yordam berish sizni quvontiradimi?",
    "13. Iqtisodiy hisob-kitoblar bilan shug'ullanish-chi?",
    "14. Sahnada chiqish qilishdan qo'rqmaysizmi?",
    "15. Tabiat va hayvonlarni o'rganish yoqadimi?",
    "16. Chet tillarini o'rganishga moyilligingiz bormi?",
    "17. Qurilish yoki arxitektura loyihalari qiziqmi?",
    "18. Psixologik kitoblar o'qiysizmi?",
    "19. Sotuv yoki marketing sohasiga qanday qaraysiz?",
    "20. Sport bilan muntazam shug'ullanasizmi?"
]

class QuizState(StatesGroup):
    answering = State()

async def handle(request):
    return web.Response(text="Maktab maslahatchisi faol!")

# --- DOIMIY ASOSIY MENYU ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="🧠 Ruhiy ko'mak")
    builder.button(text="📚 Foydali linklar")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def quiz_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data="score_1")
    builder.button(text="❌ Yo'q", callback_data="score_0")
    builder.adjust(2)
    return builder.as_markup()

# --- BOT LOGIKASI ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"🌟 Salom {message.from_user.first_name}!\nMen 6-maktab **Maktab maslahatchisi**man. "
        "Sizga o'qishingiz va kelajagingizda yordam berishga tayyorman.", 
        reply_markup=main_menu()
    )

# 1. Kasb tanlash (Siz so'ragan AI javob)
@dp.message(F.text == "🔍 Kasb tanlash")
async def ai_career_advice(message: types.Message):
    await message.answer(
        "🤖 **Maktab maslahatchisi (AI):**\n\n"
        "Kelajakni hozirdan rejalashtirish muhim! Sizning qiziqishlaringiz va qobiliyatlaringizga "
        "mos keladigan eng istiqbolli kasblarni tahlil qilishga tayyorman. Qaysi yo'nalish sizni ko'proq jalb qiladi?"
    )

# 2. Ota-onalar uchun (Siz so'ragan AI javob)
@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def ai_parents_support(message: types.Message):
    await message.answer(
        "🤖 **Maktab maslahatchisi (AI):**\n\n"
        "Hurmatli ota-onalar! Farzandingizning ta'lim jarayoni va ruhiy xotirjamligi biz uchun ustuvor vazifa. "
        "Ular bilan samarali muloqot qilish va o'qishga bo'lgan qiziqishini oshirish bo'yicha maslahatlar bera olaman."
    )

# 3. O'qituvchilar uchun (Siz so'ragan AI javob)
@dp.message(F.text == "👨‍🏫 O'qituvchilar uchun")
async def ai_teachers_help(message: types.Message):
    await message.answer(
        "🤖 **Maktab maslahatchisi (AI):**\n\n"
        "Assalomu alaykum, aziz ustoz! Dars jarayonini yanada qiziqarli qilish va zamonaviy "
        "pedagogik texnologiyalardan foydalanish bo'yicha metodik yordamga tayyorman."
    )

# 4. Testlar va so'rovnomalar (Siz so'ragan AI javob + Testni boshlash)
@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def ai_testing_center(message: types.Message, state: FSMContext):
    await message.answer(
        "🤖 **Maktab maslahatchisi (AI):**\n\n"
        "O'z bilimingiz va psixologik holatingizni tekshirib ko'rishga tayyormisiz? "
        "Hozir biz 20 ta savoldan iborat kasbiy moyillik testini boshlaymiz."
    )
    await state.update_data(current_q=0, total_score=0)
    await message.answer(f"Savol 1/20:\n\n{QUESTIONS[0]}", reply_markup=quiz_inline())
    await state.set_state(QuizState.answering)

# --- TEST JARAYONI ---
@dp.callback_query(QuizState.answering)
async def process_quiz(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data.get('current_q')
    total_score = data.get('total_score') + int(callback.data.split("_")[1])
    
    current_q += 1
    if current_q < len(QUESTIONS):
        await state.update_data(current_q=current_q, total_score=total_score)
        await callback.message.edit_text(f"Savol {current_q+1}/20:\n\n{QUESTIONS[current_q]}", reply_markup=quiz_inline())
    else:
        await state.clear()
        result = "🔥 Ajoyib! "
        if total_score >= 15: result += "Sizda yetakchilik va texnik qobiliyat kuchli."
        elif total_score >= 8: result += "Siz ko'proq ijtimoiy va gumanitar sohalarga moyilsiz."
        else: result += "Siz ijodiy va tinch ishlarni yoqtirasiz."
        
        await callback.message.edit_text(f"🏁 Test yakunlandi!\nTo'plangan ball: {total_score}\n\nNatija: {result}")
    await callback.answer()

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
