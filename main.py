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
TOKEN = "7919823792:AAENu9_-FPxLRRYs5ni5TqS1LyR3CZVlGyg"
ADMIN_ID = 8323916383 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HOLATLAR (FSM) ---
class QuizState(StatesGroup):
    answering = State()

class SupportState(StatesGroup):
    waiting_for_msg = State()

# --- SAVOLLAR BAZASI (40 TA) ---
QUESTIONS = [
    "1. Murakkab texnik chizmalarni tushunish yoqadimi?", "2. Insonlar psixologiyasini o'rganish qiziqmi?",
    "3. Algoritmlar ustida ishlash-chi?", "4. Katta jamoani boshqarish-chi?",
    "5. Matematik modellashtirish-chi?", "6. Tez muloqotga kirishish-chi?",
    "7. Grafik dizaynga qiziqasizmi?", "8. Mikroskop ostida tadqiqot-chi?",
    "9. Strategik rejalashtirish-chi?", "10. Matnlarni chuqur tahlil qilish-chi?",
    "11. Robototexnika qiziqmi?", "12. Ijtimoiy loyihalarda qatnashish-chi?",
    "13. Moliyaviy tahlil-chi?", "14. Auditoriya oldida nutq so'zlash-chi?",
    "15. Ekologiya va tabiat-chi?", "16. Xorijiy tillarda ijod-chi?",
    "17. Arxitektura loyihalari-chi?", "18. Ruhiy dalda berish-chi?",
    "19. Bozor tahlili-chi?", "20. Jismoniy chidamlilik-chi?",
    "21. Sun'iy intellekt yaratish-chi?", "22. Pedagogik metodika-chi?",
    "23. Big Data bilan ishlash-chi?", "24. Siyosiy jarayonlar-chi?",
    "25. Kvant fizikasi qiziqmi?", "26. Mijozlar ehtiyojini sezish-chi?",
    "27. Liboslar dizayni-chi?", "28. Biotexnologiya-chi?",
    "29. Startap loyihalar-chi?", "30. Jurnalistik surishtiruv-chi?",
    "31. Avtomatlashtirilgan tizimlar-chi?", "32. Volontyorlik-chi?",
    "33. Buxgalteriya-chi?", "34. Kreativ reklama-chi?",
    "35. Tibbiy tashxis qo'yish-chi?", "36. Huquqshunoslik-chi?",
    "37. Landshaft dizayni-chi?", "38. Mikrobiologik tajribalar-chi?",
    "39. Muzokaralar olib borish-chi?", "40. VR olami qiziqmi?"
]

async def handle(request):
    return web.Response(text="Bot faol!")

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
    await message.answer(f"🌟 Salom {message.from_user.first_name}! Men 6-maktab **Maktab maslahatchisi**man.", reply_markup=main_menu())

@dp.message(F.text == "🔍 Kasb tanlash")
async def career_advice(message: types.Message):
    text = ("🎯 **Kasb tanlash bo'yicha maslahatlar:**\n\n"
            "• **O'zingizni taning:** Qaysi fanlar sizga osonroq? Nima bilan soatlab shug'ullana olasiz?\n"
            "• **Bozorni o'rganing:** Kelajakda IT, biotexnologiya va 'yashil' energiya sohalari eng talabgir bo'ladi.\n"
            "• **Amaliyot qiling:** Tanlagan sohangiz bo'yicha mutaxassislar bilan gaplashing.\n\n"
            "🚀 **Zamonaviy kasblar:** AI muhandisi, Data Scientist, Kiberxavfsizlik tahlilchisi.")
    await message.answer(text)

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents_advice(message: types.Message):
    text = ("👨‍👩‍👧‍👦 **Hurmatli ota-onalar uchun tavsiyalar:**\n\n"
            "⚠️ **Xatolardan qoching:**\n"
            "1. Farzandni o'zingiz yetishmagan orzularga majburlamang.\n"
            "2. Faqat 'nufuzli' deb hisoblangan eski kasblarga qotib qolmang.\n\n"
            "✅ **Nima qilish kerak?**\n"
            "— Farzandingizning qobiliyati va xohishini birinchi o'ringa qo'ying.\n"
            "— Uni tanqid qilmang, aksincha turli sohalarni sinab ko'rishiga sharoit yarating.")
    await message.answer(text)

@dp.message(F.text == "📞 Maslahatchi bilan bog'lanish")
async def support_start(message: types.Message, state: FSMContext):
    await message.answer("📝 Iltimos, o'z g'oyangiz, taklifingiz yoki savolingizni yozib yuboring. Men uni maslahatchiga yetkazaman.")
    await state.set_state(SupportState.waiting_for_msg)

@dp.message(SupportState.waiting_for_msg)
async def support_received(message: types.Message, state: FSMContext):
    # Adminga xabar yuborish
    try:
        await bot.send_message(
            ADMIN_ID, 
            f"📩 **Yangi murojaat!**\n\n"
            f"👤 **Kimdan:** {message.from_user.full_name}\n"
            f"🆔 **ID:** {message.from_user.id}\n"
            f"✍️ **Xabar:** {message.text}"
        )
        await message.answer("✅ Xabaringiz yuborildi! Maslahatchi tez orada ko'rib chiqadi.")
    except Exception as e:
        await message.answer("❌ Xabarni yuborishda xatolik yuz berdi. Keyinroq urinib ko'ring.")
    await state.clear()

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_start(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data="ans_1")
    builder.button(text="❌ Yo'q", callback_data="ans_0")
    await message.answer("🚀 **Professional diagnostika (40 ta savol)**\n\n" + QUESTIONS[0], reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def quiz_step(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data.get('current_q'), data.get('total_score') + int(callback.data.split("_")[1])
    curr += 1
    
    if curr < len(QUESTIONS):
        await state.update_data(current_q=curr, total_score=score)
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Ha", callback_data="ans_1")
        builder.button(text="❌ Yo'q", callback_data="ans_0")
        await callback.message.edit_text(f"Savol {curr+1}/40:\n\n{QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        await state.clear()
        res = "Sizda tahliliy fikrlash kuchli!" if score > 25 else "Siz ko'proq ijodiy inson ekansiz."
        await callback.message.edit_text(f"🏁 Test yakunlandi!\nBall: {score}/40\n\n{res}")
    await callback.answer()

# Qolgan bo'limlar uchun oddiy javoblar
@dp.message(F.text.in_(["🧠 Ruhiy ko'nikma", "👨‍🏫 O'qituvchilar uchun", "📚 Foydali linklar"]))
async def other_sections(message: types.Message):
    await message.answer("🤖 Ushbu bo'lim boyitilmoqda. Maslahatlar va linklar tez orada yuklanadi.")

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
