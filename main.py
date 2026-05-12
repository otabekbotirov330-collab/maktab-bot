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
TOKEN = "7919823792:AAHPiBXqWfLaoPLYqGs0vlxrYkcxUhH7OHI"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- MA'LUMOTLAR BAZASI ---
QUESTIONS = [
    "1. Texnik qurilmalarni ta'mirlash yoqadimi?", "2. Insonlarga maslahat berishni yoqtirasizmi?",
    "3. Kompyuter dasturlarini o'rganish qiziqarli-mi?", "4. Tadbirlar tashkil qilishni yoqtirasizmi?",
    "5. Matematik masalalarni yechish yoqadimi?", "6. Yangi insonlar bilan tanishish osonmi?",
    "7. Chizmachilik yoki dizayn yoqadimi?", "8. Laboratoriyada tajribalar o'tkazishni xohlaysizmi?",
    "9. Jamoani boshqarish yoqadimi?", "10. Kitob tahlil qilishni yoqtirasizmi?",
    "11. Avtomobillar mexanizmiga qiziqasizmi?", "12. Kasallarga yordam berish quvontiradimi?",
    "13. Iqtisodiy hisob-kitoblar qiziqarli-mi?", "14. Sahnada chiqish qilishdan qo'rqmaysizmi?",
    "15. Tabiatni o'rganish yoqadimi?", "16. Chet tillarini o'rganishga moyillik bormi?",
    "17. Arxitektura loyihalari qiziqmi?", "18. Psixologik kitoblar o'qiysizmi?",
    "19. Marketing sohasiga qiziqasizmi?", "20. Sport bilan shug'ullanasizmi?",
    "21. Robotlar yasashni xohlarmidingiz?", "22. Bolalarga dars berish yoqadimi?",
    "23. Ma'lumotlar bazasi bilan ishlash-chi?", "24. Nutq so'zlashni yoqtirasizmi?",
    "25. Fizika qonunlarini o'rganish qiziqmi?", "26. Mijozlarga xizmat ko'rsatish yoqadimi?",
    "27. Tikuvchilik yoki hunarmandchilik-chi?", "28. Kimyoviy elementlarni o'rganish-chi?",
    "29. Biznes g'oyalar o'ylab topasizmi?", "30. Maqolalar yozishni yoqtirasizmi?",
    "31. Elektr asboblarini tushunasizmi?", "32. Ijtimoiy loyihalarda qatnashasizmi?",
    "33. Grafiklarni tahlil qilish yoqadimi?", "34. Reklama roliklari yaratish-chi?",
    "35. Astronomiya qiziqarli-mi?", "36. Huquq va qonunlarni o'rganish-chi?",
    "37. Interyer dizayni yoqadimi?", "38. Biologik tajribalar qiziqmi?",
    "39. Sotuv rejasini tuzish-chi?", "40. Shaxmat o'ynashni yoqtirasizmi?"
]

class QuizState(StatesGroup):
    answering = State()

async def handle(request):
    return web.Response(text="Maktab maslahatchisi faol!")

# --- MENYU TUZILISHI ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="🧠 Ruhiy ko'nikma")
    builder.button(text="📚 Foydali linklar")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"🌟 Salom {message.from_user.first_name}! Men **Maktab maslahatchisi**man.", reply_markup=main_menu())

@dp.message(F.text == "🔍 Kasb tanlash")
async def modern_jobs(message: types.Message):
    text = ("🚀 **Zamonaviy kasblar haqida ma'lumot:**\n\n"
            "1. **Data Scientist** — Ma'lumotlar asosida bashorat qiluvchi mutaxassis.\n"
            "2. **Robototexnika muhandisi** — Avtomatlashtirilgan tizimlarni yaratuvchi.\n"
            "3. **UI/UX Dizayner** — Sayt va ilovalarning qulayligini ta'minlovchi.\n"
            "4. **Raqamli marketolog** — Internetda brendlarni targ'ib qiluvchi.")
    await message.answer(text)

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents_advice(message: types.Message):
    text = ("⚠️ **Kasb tanlashda ota-onalar yo'l qo'yadigan xatolar:**\n\n"
            "❌ *Majburlash:* Farzandning qiziqishiga qaramasdan o'z orzusini amalga oshirish.\n"
            "❌ *Moddiy manfaat:* Faqat ko'p pul topadigan kasbga yo'naltirish.\n\n"
            "✅ **Tavsiyalar:**\n"
            "— Farzandingizning kuchli tomonlarini kuzating.\n"
            "— Turli soha vakillari bilan suhbatlar tashkil qilib bering.")
    await message.answer(text)

@dp.message(F.text == "🧠 Ruhiy ko'nikma")
async def psycho_skills(message: types.Message):
    text = ("🧘 **Kasbga ruhiy tayyorgarlik:**\n\n"
            "1. **Intizom:** Har kuni o'z ustingizda ishlashni odat qiling.\n"
            "2. **Stressga chidamlilik:** Xatolarni dars deb biling.\n"
            "3. **Muloqot:** Insonlar bilan ochiq suhbatlashishni o'rganing.")
    await message.answer(text)

@dp.message(F.text == "👨‍🏫 O'qituvchilar uchun")
async def teachers_guide(message: types.Message):
    text = ("👨‍🏫 **Darsni qiziqarli tashkil etish:**\n\n"
            "• **Gamifikatsiya:** Darsga o'yin elementlarini kiriting.\n"
            "• **Interaktivlik:** Kahoot yoki Wordwall kabi resurslardan foydalaning.\n"
            "• **Loyiha usuli:** O'quvchilarga kichik jamoaviy loyihalar bering.")
    await message.answer(text)

@dp.message(F.text == "📚 Foydali linklar")
async def useful_links(message: types.Message):
    text = ("📚 **Ta'lim va kasb tanlash portallari:**\n\n"
            "🔗 [Uzbmb.uz](https://my.uzbmb.uz) — OTMga kirish.\n"
            "🔗 [Kundalik.com](https://kundalik.com) — Maktab tizimi.\n"
            "🔗 [Khan Academy](https://uz.khanacademy.org) — Bepul bilim olish.")
    await message.answer(text, disable_web_page_preview=True)

# --- 40 TALIK TEST JARAYONI ---
@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def start_quiz(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    await message.answer("📝 **Professional test (40 ta savol)**\n\n" + QUESTIONS[0], 
                         reply_markup=InlineKeyboardBuilder().button(text="✅ Ha", callback_data="s_1").button(text="❌ Yo'q", callback_data="s_0").as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def process_quiz(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data.get('current_q'), data.get('total_score') + int(callback.data.split("_")[1])
    curr += 1
    
    if curr < len(QUESTIONS):
        await state.update_data(current_q=curr, total_score=score)
        await callback.message.edit_text(f"Savol {curr+1}/40:\n\n{QUESTIONS[curr]}", 
                                         reply_markup=InlineKeyboardBuilder().button(text="✅ Ha", callback_data="s_1").button(text="❌ Yo'q", callback_data="s_0").as_markup())
    else:
        await state.clear()
        res = "🚀 Sizda yuqori salohiyat bor! " + ("Texnik sohalar sizniki." if score > 25 else "Gumanitar sohalar sizniki.")
        await callback.message.edit_text(f"🏁 Test yakunlandi!\nBall: {score}/40\n\n{res}")
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
