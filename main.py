import os, asyncio, logging, pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAFnn3CFMjMND-d26m6Svp1J_UyVgh3SEC0" 
ADMIN_ID = 8323916383 
DATA_FOLDER = "reports" 
CERT_FOLDER = "temp_certs"

for f in [DATA_FOLDER, CERT_FOLDER]:
    if not os.path.exists(f): os.makedirs(f)

EXCEL_FILE = os.path.join(DATA_FOLDER, "umumiy_hisobot.xlsx")

logging.basicConfig(level=logging.INFO)
bot, dp = Bot(token=TOKEN), Dispatcher()

class QuizState(StatesGroup):
    waiting_name = State()
    answering = State()

# --- 40 TA SAVOL (KASBIY MOYILLIKNI ANIQLASH) ---
QUESTIONS = [
    "1. Texnik qurilmalarni qismlarga ajratib, ularni qayta yig'ishni yoqtirasizmi?",
    "2. Kompyuter dasturlari va mobil ilovalar yaratishga qiziqasizmi?",
    "3. Odamlarga psixologik maslahatlar berish sizga yoqadimi?",
    "4. Yangi biznes g'oyalar ustida ishlashni xohlaysizmi?",
    "5. Tabiat va o'simliklar dunyosini tadqiq qilish sizga qiziqmi?",
    "6. Video montaj va kreativ kontentlar yaratishni yoqtirasizmi?",
    "7. Matematik masalalarni yechish sizga zavq beradimi?",
    "8. Chet tillarini o'rganish va tarjimonlik qilishga qiziqasizmi?",
    "9. Robototexnika va avtomatlashtirilgan tizimlarga qiziqishingiz bormi?",
    "10. O'z jamoangizga rahbarlik qilishni yoqtirasizmi?",
    "11. Tibbiyot va inson salomatligini o'rganish sizga yoqadimi?",
    "12. Tasviriy san'at va dizayn yo'nalishida iqtidoringiz bormi?",
    "13. Fizika qonuniyatlarini amalda sinab ko'rishga qiziqasizmi?",
    "14. Logika va mantiqiy o'yinlarni o'ynashni yoqtirasizmi?",
    "15. Qishloq xo'jaligi texnologiyalarini o'rganishni xohlaysizmi?",
    "16. Ma'lumotlarni tahlil qilish va statistikaga qiziqasizmi?",
    "17. Ijtimoiy loyihalarda ko'ngilli sifatida qatnashishni yoqtirasizmi?",
    "18. Arxitektura va bino loyihalarini chizishga qiziqasizmi?",
    "19. Kimyoviy tajribalar o'tkazish sizga yoqadimi?",
    "20. Huquqshunoslik va qonunlarni o'rganishga qiziqasizmi?",
    "21. Kosmos va astronomiya sirlari sizga qiziqmi?",
    "22. Fotoapparat bilan ishlash va suratga olishni yoqtirasizmi?",
    "23. Iqtisodiyot va moliya bozorini kuzatishni yoqtirasizmi?",
    "24. Bolalar bilan ishlash va ularga dars berishni xohlaysizmi?",
    "25. Qurilish materiallari va ularning xususiyatlari qiziqmi?",
    "26. Musiqa yaratish yoki musiqa asboblarida chalishni yoqtirasizmi?",
    "27. Sun'iy intellekt va neyrotarmoqlar bilan ishlashga qiziqasizmi?",
    "28. Siyosat va xalqaro munosabatlar sizga qiziqmi?",
    "29. Ekologik muammolarni hal qilishda ishtirok etishni xohlaysizmi?",
    "30. Sport bilan professional shug'ullanishni yoqtirasizmi?",
    "31. Kitob o'qish va adabiy asarlar tahlili sizga yoqadimi?",
    "32. Avtomobil dvigatellarining ishlash prinsipi qiziqmi?",
    "33. Sotuv va marketing sohasida ishlashni xohlaysizmi?",
    "34. Geografiya va sayohat qilishni yoqtirasizmi?",
    "35. Oshpazlik va yangi retseptlar yaratish sizga yoqadimi?",
    "36. Tarixiy voqealarni o'rganish va tahlil qilish qiziqmi?",
    "37. Jurnalistika va intervyu olishni yoqtirasizmi?",
    "38. Tikuvchilik va moda dizayniga qiziqasizmi?",
    "39. Dasturlash tillaridan birini o'rganishni boshlaganmisiz?",
    "40. Kelajakda o'z startapingizga ega bo'lishni orzu qilasizmi?"
]

# --- SERTIFIKAT GENERATSIYASI ---
def create_certificate(full_name, direction):
    template_path = "template.png"
    if not os.path.exists(template_path): return None
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    try:
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_info = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except: font_name = font_info = ImageFont.load_default()

    draw.text((630, 465), full_name.upper(), fill=(212, 175, 55), font=font_name, anchor="mm")
    draw.text((700, 740), datetime.now().strftime("%d.%m.%Y"), fill=(255, 255, 255), font=font_info)
    path = os.path.join(CERT_FOLDER, f"cert_{datetime.now().timestamp()}.png")
    img.save(path)
    return path

# --- EXCEL ---
def save_to_report(name, user_id, answers, result):
    data = {"Sana": [datetime.now()], "ID": [user_id], "F.I.SH": [name], "Javoblar": [str(answers)], "Natija": [result]}
    df_new = pd.DataFrame(data)
    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else: df_final = df_new
    df_final.to_excel(EXCEL_FILE, index=False)
    return EXCEL_FILE

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Kasbiy so'rovnoma")
    builder.button(text="📞 Bog'lanish")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.adjust(1)
    await m.answer("Assalomu alaykum! 'StartUp Maktab' botiga xush kelibsiz.", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "📞 Bog'lanish")
async def contact_info(m: types.Message):
    text = (
        "📞 **Bog'lanish uchun ma'lumotlar:**\n\n"
        "👤 **Maslahatchi:** Otabek Bakhtiyorovich Botirov\n"
        "🏫 **Manzil:** Rishton tumani, 6-sonli maktab\n"
        "📧 **Telegram:** @J780wa"
        "🌐 **Loyiha:** StartUp Maktab"
    )
    await m.answer(text)

@dp.message(F.text == "📝 Kasbiy so'rovnoma")
async def start_quiz(m: types.Message, state: FSMContext):
    await m.answer("Sertifikat uchun to'liq ism-familiyangizni kiriting:")
    await state.set_state(QuizState.waiting_name)

@dp.message(QuizState.waiting_name)
async def get_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text, answers=[], curr=0)
    builder = InlineKeyboardBuilder().button(text="Boshlash 🚀", callback_data="start_test")
    await m.answer(f"Rahmat, {m.text}. 40 ta savoldan iborat so'rovnomani boshlaymizmi?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "start_test")
@dp.callback_query(QuizState.answering)
async def handle_quiz(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers', [])
    if "ans_" in c.data:
        answers.append("Ha" if c.data == "ans_1" else "Yo'q")
    
    curr = len(answers)
    if curr < len(QUESTIONS):
        await state.update_data(answers=answers)
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Ha", callback_data="ans_1").button(text="❌ Yo'q", callback_data="ans_0")
        await c.message.edit_text(f"{curr+1}-savol: {QUESTIONS[curr]}", reply_markup=builder.as_markup())
        await state.set_state(QuizState.answering)
    else:
        name, score = data['name'], answers.count("Ha")
        res_dir = "STEM va Yuqori Texnologiyalar" if score > 25 else "Gumanitar va Ijtimoiy soha"
        save_to_report(name, c.from_user.id, answers, res_dir)
        cert_path = create_certificate(name, res_dir)
        await c.message.delete()
        if cert_path: await bot.send_photo(c.from_user.id, photo=FSInputFile(cert_path), caption="🎉 Tabriklaymiz! Sertifikatingiz tayyor.")
        await bot.send_document(ADMIN_ID, document=FSInputFile(EXCEL_FILE), caption=f"📊 Yangi hisobot: {name}")
        await state.clear()

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
