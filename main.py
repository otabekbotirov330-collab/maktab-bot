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
TOKEN = "7919823792:AAGxEVxU2fzXca-kxPCsVDpUEI4gPwyKJIc"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HOLATLAR ---
class QuizState(StatesGroup):
    answering = State()

class SupportState(StatesGroup):
    waiting_for_msg = State()

# --- 40 TA MURAKKAB SAVOL ---
QUESTIONS = [
    "1. Murakkab texnik chizmalarni tushunish yoqadimi?", "2. Insonlar psixologiyasini o'rganish qiziqmi?",
    "3. Algoritmlar ustida ishlash yoqadimi?", "4. Jamoani boshqarish mas'uliyatini olasizmi?",
    "5. Matematik modellashtirish qiziqarli-mi?", "6. Tez muloqotga kirishish sizga osonmi?",
    "7. Grafik dizayn va estetika yoqadimi?", "8. Laboratoriya tadqiqotlari qiziqmi?",
    "9. Strategik rejalashtirish yoqadimi?", "10. Matnlarni chuqur tahlil qilasizmi?",
    "11. Robototexnika yoqadimi?", "12. Ijtimoiy muammolarni hal qilish-chi?",
    "13. Moliyaviy prognozlar qilish qiziqmi?", "14. Nutq so'zlash sizga osonmi?",
    "15. Tabiatni muhofaza qilish yoqadimi?", "16. Chet tillarida ijod qilish-chi?",
    "17. Arxitektura loyihalari qiziqmi?", "18. Insonlarga ruhiy dalda berish-chi?",
    "19. Bozor tahlili yoqadimi?", "20. Jismoniy mehnatga tayyormisiz?",
    "21. Sun'iy intellekt yaratish-chi?", "22. Pedagogik metodika yoqadimi?",
    "23. Big Data bilan ishlash-chi?", "24. Siyosiy jarayonlar qiziqmi?",
    "25. Kvant fizikasi yoqadimi?", "26. Mijozlar ehtiyojini sezish-chi?",
    "27. Liboslar dizayni yoqadimi?", "28. Biotexnologiya qiziqmi?",
    "29. Startaplarni boshqarish-chi?", "30. Jurnalistika yoqadimi?",
    "31. Avtomatlashtirilgan tizimlar-chi?", "32. Volontyorlik yoqadimi?",
    "33. Buxgalteriya va hisob-kitob-chi?", "34. Kreativ reklama g'oyalari-chi?",
    "35. Tibbiy tashxis qo'yish jarayoni-chi?", "36. Huquqshunoslik yoqadimi?",
    "37. Landshaft dizayni qiziqmi?", "38. Mikrobiologik tajribalar-chi?",
    "39. Muzokaralar olib borish yoqadimi?", "40. VR texnologiyalari qiziqmi?"
]

async def handle(request):
    return web.Response(text="Metodik Bot Live holatda!")

# --- ASOSIY MENYU ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="🧠 Ruhiy ko'nikma")
    builder.button(text="📚 Foydali linklar")
    builder.button(text="📞 Maslahatchi bilan bog'lanish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- HANDLERLAR ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"🌟 Salom {message.from_user.first_name}! Men professional **Maktab maslahatchisi** botiman. Bo'limlardan birini tanlang:", reply_markup=main_menu())

@dp.message(F.text == "🔍 Kasb tanlash")
async def career_section(message: types.Message):
    text = ("🎯 **Kasb tanlash bo'yicha aniq tavsiyalar:**\n\n"
            "✅ **1. Qobiliyatingizni aniqlang:** Agar matematika yoqsa - IT yoki muhandislik; agar odamlar bilan ishlash yoqsa - pedagogika yoki psixologiya.\n"
            "✅ **2. Zamonaviy kasblarni tanlang:** Kelajakda AI mutaxassisi, kiberxavfsizlik va yashil energetika sohalari eng yuqori maoshli bo'ladi.\n"
            "✅ **3. 'Soft Skills'ni unutmang:** Qaysi kasb bo'lishidan qat'iy nazar, muloqot va tanqidiy fikrlash hal qiluvchi rol o'ynaydi.")
    await message.answer(text)

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents_section(message: types.Message):
    text = ("👨‍👩‍👧‍👦 **Ota-onalar uchun metodik tavsiyalar:**\n\n"
            "🛑 **Asosiy xato:** Farzandni o'zingiz erisha olmagan orzularingizni amalga oshirishga majburlash.\n"
            "🛑 **Xato:** Faqat moddiy jihatdan foydali ko'ringan, lekin farzandga yoqmaydigan kasbni tanlash.\n\n"
            "✅ **To'g'ri yondashuv:** Farzandingizni kuzating, u nima bilan shug'ullanganda vaqt o'tganini sezmay qoladi? Aynan shu uning haqiqiy qiziqishi hisoblanadi.")
    await message.answer(text)

@dp.message(F.text == "👨‍🏫 O'qituvchilar uchun")
async def teachers_section(message: types.Message):
    text = ("👨‍🏫 **Darsni qiziqarli tashkil etish usullari:**\n\n"
            "• **Pizmoniy tanaffuslar:** Dars o'rtasida 2 daqiqalik harakatli o'yinlar diqqatni oshiradi.\n"
            "• **Gamifikatsiya:** Mavzuni Kahoot yoki Wordwall orqali o'yin ko'rinishida tushuntiring.\n"
            "• **Muammoli ta'lim:** O'quvchilarga tayyor javobni emas, yechilishi kerak bo'lgan real hayotiy muammoni bering.")
    await message.answer(text)

@dp.message(F.text == "🧠 Ruhiy ko'nikma")
async def psychology_section(message: types.Message):
    text = ("🧠 **Kasbiy va shaxsiy ruhiy ko'nikmalar:**\n\n"
            "1. **Stressga chidamlilik:** Har qanday xatoni 'muvaffaqiyatsizlik' emas, 'tajriba' deb qabul qiling.\n"
            "2. **Vaqtni boshqarish:** Pomodoro texnikasidan foydalaning (25 daqiqa ish, 5 daqiqa dam).\n"
            "3. **Ijobiy vizualizatsiya:** Kelajakdagi ish joyingizni va undagi muvaffaqiyatingizni har kuni 5 daqiqa tasavvur qiling.")
    await message.answer(text)

@dp.message(F.text == "📚 Foydali linklar")
async def links_section(message: types.Message):
    text = ("📚 **Ishonchli va foydali portallar:**\n\n"
            "🔗 [Uzbmb.uz](https://my.uzbmb.uz) — Davlat test markazi.\n"
            "🔗 [Coursera](https://www.coursera.org) — Jahon kurslari.\n"
            "🔗 [Khan Academy](https://uz.khanacademy.org) — Bepul bilimlar.\n"
            "🔗 [It-park.uz](https://it-park.uz) — IT ta'limi.")
    await message.answer(text, disable_web_page_preview=True)

@dp.message(F.text == "📞 Maslahatchi bilan bog'lanish")
async def support_start(message: types.Message, state: FSMContext):
    await message.answer("✍️ G'oya, taklif yoki savolingizni yozing. Men uni maslahatchi Otabek Botirovga yetkazaman:")
    await state.set_state(SupportState.waiting_for_msg)

@dp.message(SupportState.waiting_for_msg)
async def support_done(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 **Yangi murojaat!**\n👤: {message.from_user.full_name}\n✍️: {message.text}")
    await message.answer("✅ Xabaringiz yuborildi. Rahmat!")
    await state.clear()

# --- TEST LOGIKASI ---
@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_start(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data="q_1")
    builder.button(text="❌ Yo'q", callback_data="q_0")
    await message.answer("📝 **Professional test boshlandi (40 ta savol)**\n\n" + QUESTIONS[0], reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def quiz_step(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data.get('current_q'), data.get('total_score') + int(callback.data.split("_")[1])
    curr += 1
    
    if curr < len(QUESTIONS):
        await state.update_data(current_q=curr, total_score=score)
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Ha", callback_data="q_1")
        builder.button(text="❌ Yo'q", callback_data="q_0")
        await callback.message.edit_text(f"Savol {curr+1}/40:\n\n{QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        await state.clear()
        res = "🌟 Yuqori salohiyat! Siz murakkab muammolarni yechishga moyilsiz." if score > 30 else "💡 Sizda ijtimoiy va ijodiy qobiliyatlar ustun."
        await callback.message.edit_text(f"🏁 Test yakunlandi!\nNatija: {score}/40 ball.\n\n{res}")
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
