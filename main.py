import os
import asyncio
import logging
import pandas as pd
from datetime import datetime
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAHijlxUSUWanNTKY9L4oCvaOVHf5FE7tuY"
ADMIN_ID = 8323916383 
EXCEL_FOLDER = "test_results"

if not os.path.exists(EXCEL_FOLDER):
    os.makedirs(EXCEL_FOLDER)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class QuizState(StatesGroup):
    answering = State()

# --- 50 TA PROFESSIONAL SAVOL ---
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
    "39. Muzokaralar olib borish yoqadimi?", "40. VR texnologiyalari qiziqmi?",
    "41. Avtomobillarni ta'mirlash sizga yoqadimi?", "42. Ijtimoiy tarmoqlar uchun kontent yaratish-chi?",
    "43. Kosmik texnologiyalar va astronomiya-chi?", "44. Tarixiy hujjatlar bilan ishlash yoqadimi?",
    "45. Sayyohlik yo'nalishlarini ishlab chiqish-chi?", "46. Oshpazlik sirlarini o'rganish yoqadimi?",
    "47. Audio-video montaj ishlari-chi?", "48. Ekologik muammolarni hal qilish yoqadimi?",
    "49. Logistika va tashuvlarni rejalashtirish-chi?", "50. Blockchain va kriptovalyutalar qiziqmi?"
]

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.button(text="📞 Maslahatchi bilan bog'lanish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- EXCEL FUNKSIYASI ---
def save_to_excel(user_id, full_name, score):
    file_path = os.path.join(EXCEL_FOLDER, "natijalar.xlsx")
    data = {"Sana": [datetime.now()], "ID": [user_id], "Ism": [full_name], "Ball": [score]}
    df_new = pd.DataFrame(data)
    if os.path.exists(file_path):
        df_old = pd.read_excel(file_path)
        df_new = pd.concat([df_old, df_new], ignore_index=True)
    df_new.to_excel(file_path, index=False)
    return file_path

# --- HANDLERLAR ---

@dp.message(F.text == "🔍 Kasb tanlash")
async def career_section(message: types.Message):
    tips = [f"{i}. " + t for i, t in enumerate([
        "IKIGAI metodini o'rganing.", "Mehnat bozorini tahlil qiling.", "IT sohasini chetlab o'tmang.",
        "Xorijiy tillar - bu kalit.", "Yumshoq ko'nikmalarni (soft skills) rivojlantiring.",
        "Mentor toping.", "Stajirovkalarga boring.", "Shaxsiy portfolio yarating.",
        "Sohaviy tadbirlarda qatnashing.", "Tanqidiy fikrlashni o'stiring.", "Vaqtni boshqarishni o'rganing.",
        "Networking (tanish-bilish) qiling.", "Kreativlikni oshiring.", "Sun'iy intellektdan foydalaning.",
        "O'z loyihangizni boshlang.", "Kasbiy testlardan o'ting.", "Psixolog maslahatini oling.",
        "Dunyo trendlarini kuzating.", "O'qishdan to'xtamang.", "Sog'liqni saqlang.",
        "Maqsadni SMART bo'yicha qo'ying.", "Xatodan qo'rqmang.", "Tadbirkorlikni o'rganing.",
        "SMM ko'nikmalarini oling.", "Ma'lumotlar tahlilini o'rganing.", "Ekologik kasblarni ko'ring.",
        "Masofaviy ishlashni sinang.", "Shaxsiy brend yarating.", "Jamoada ishlashni o'rganing.",
        "Nutq mahoratini oshiring.", "Liderlikni rivojlantiring.", "Dizayn asoslarini biling.",
        "Mobil ilovalar yarating.", "Kiberxavfsizlikka qiziqing.", "Bulutli texnologiyalarni biling.",
        "Kitob o'qing.", "Podkastlarni tinglang.", "Onlayn kurslarda o'qing.",
        "Ekspert bo'ling.", "Xatolar ustida ishlang.", "Sayohat qiling.",
        "Yangi madaniyatlarni o'rganing.", "Hobbini kasbga aylantiring.", "Daromadni rejalashtiring.",
        "Investitsiyani o'rganing.", "EQ (Emotsional intellekt)ni oshiring.", "Robototexnikaga qiziqing.",
        "Bio-texnologiyalarni ko'ring.", "Blockchainni o'rganing.", "Doim izlanishda bo'ling."
    ], 1)]
    await message.answer("🎯 **Kasb tanlash bo'yicha 50 ta maslahat:**\n\n" + "\n".join(tips))

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents_section(message: types.Message):
    tips = [f"{i}. " + t for i, t in enumerate([
        "Farzandingizni eshiting.", "Uning qiziqishini qo'llab-quvvatlang.", "Uni majburlamang.",
        "O'z orzungizni unga yuklamang.", "Sohalarni birga tahlil qiling.", "Tinch muhit yarating.",
        "Iste'dodini aniqlang.", "Ishonch bildiring.", "Xatoga to'g'ri yondashing.",
        "Zamonaviy kasblarni o'rganing.", "Tanlov huquqini bering.", "Mentor bo'ling.",
        "O'quv markazini birga tanlang.", "Sarmoya kiriting.", "Vaqt ajrating.",
        "Do'st bo'ling.", "Yutug'ini bayram qiling.", "Sabrli bo'ling.",
        "Texnologiyani birga o'rganing.", "Kitobxonlikka undang.", "Sportga yo'naltiring.",
        "Intuitsiyaga ishoning.", "Boshqalar bilan solishtirmang.", "Namuna bo'ling.",
        "Sayohatga olib boring.", "Mustaqillikka o'rgating.", "Mas'uliyatni bering.",
        "Kelajak haqida gaplashing.", "Ko'rgazmalarga boring.", "Ochiq muloqot qiling.",
        "Hobbini hurmat qiling.", "Kreativlikni bo'g'mang.", "Darsiga yordam bering.",
        "Xotirjamlikni saqlang.", "Fikrini so'rang.", "Motivatsiya bering.",
        "Daldali bo'ling.", "Birga yechim qidiring.", "Salomatligini o'ylang.",
        "Dam olishga qo'ying.", "Nazoratni kamaytiring.", "Ishonch quring.",
        "Tajriba ulashing.", "Dunyoqarashini kengaytiring.", "Yangi bilimga undang.",
        "Kalitni ko'rsating.", "Yonida ekaningizni bildiring.", "Seving.",
        "Faxrlaning.", "Kelajagiga ishoning."
    ], 1)]
    await message.answer("👨‍👩‍👧‍👦 **Ota-onalar uchun 50 ta qoida:**\n\n" + "\n".join(tips))

@dp.message(F.text == "ℹ️ Maslahatchi haqida")
async def info_cmd(message: types.Message):
    info = [
        "👤 **F.I.SH:** Otabek Bakhtiyorovich Botirov",
        "🏫 **Lavozimi:** “Kelajak” markazlarining umumiy oʻrta ta’lim muassasalaridagi oʻquvchilar tashabbuslarini qoʻllab-quvvatlash boʻyicha maktab maslahatchisi",
        "📍 **Hudud:** Farg'ona viloyati, Rishton tumani",
        "📜 **Asos:** Oʻzbekiston Respublikasi Maktabgacha va maktab ta’limi vazirining 2026-yil “21”-apreldagi 153–sonli buyrugʻiga ILOVA",
        "📸 **Hobbisi:** Foto-video operator, sun'iy intellekt yordamida kontent yaratish",
        "🚀 **Loyiha:** 'StartUp Maktab' va @tashabbus_maktab_bot"
    ]
    await message.answer("\n".join(info))

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_start(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data="q_1")
    builder.button(text="❌ Yo'q", callback_data="q_0")
    await message.answer(f"📝 **Professional test (50 savol)**\n\n{QUESTIONS[0]}", reply_markup=builder.as_markup())
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
        await callback.message.edit_text(f"Savol {curr+1}/50:\n\n{QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        await state.clear()
        save_to_excel(callback.from_user.id, callback.from_user.full_name, score)
        await callback.message.edit_text(f"🏁 **Test tugadi!**\nNatija: {score}/50 ball.\n\nNatija Excelga saqlandi va maslahatchiga yuborildi.")
        await bot.send_message(ADMIN_ID, f"📊 **Yangi natija!**\n👤 {callback.from_user.full_name}\n🎯 Ball: {score}")
    await callback.answer()

async def main():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
