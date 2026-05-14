import os, asyncio, logging, pandas as pd
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
TOKEN = "7919823792:AAFnn3CFMjMND-d26m6Svp1J_UyVgh3SEC0"
ADMIN_ID = 8323916383 
ADMIN_FOLDER, CERT_FOLDER = "admin_data", "certificates"

for f in [ADMIN_FOLDER, CERT_FOLDER]:
    if not os.path.exists(f): os.makedirs(f)

logging.basicConfig(level=logging.INFO)
bot, dp = Bot(token=TOKEN), Dispatcher()

class QuizState(StatesGroup):
    waiting_name = State()
    answering = State()

class ContactState(StatesGroup):
    waiting_message = State()

# --- 40 TA KASBGA YO'NALTIRISH SAVOLLARI ---
QUESTIONS = [
    "1. Yangi texnologik qurilmalarni qismlarga ajratib ko'rish sizga qiziqmi?",
    "2. Odamlarga maslahat berish va ularni tinglashni yoqtirasizmi?",
    "3. Kompyuter dasturlari va o'yinlar qanday ishlashiga qiziqasizmi?",
    "4. Tabiat va ekologiya muammolari sizni tashvishga soladimi?",
    "5. Chizish, dizayn yoki kreativ g'oyalar o'ylab topish yoqadimi?",
    "6. Matematik hisob-kitoblar va mantiqiy masalalarni tez yechasizmi?",
    "7. Notiqlik va omma oldida so'zlashga moyilligingiz bormi?",
    "8. Kimyoviy elementlar va tajribalar o'tkazish qiziqmi?",
    "9. Chet tillarini o'rganish siz uchun oson kechadimi?",
    "10. Jamoani boshqarish va lider bo'lishni xohlaysizmi?",
    "11. Tibbiyot va inson tana tuzilishini o'rganish yoqadimi?",
    "12. Kosmos, yulduzlar va koinot sirlari sizni qiziqtiradimi?",
    "13. Biznes reja tuzish va pul topish yo'llarini o'ylaysizmi?",
    "14. Qurilish, arxitektura va bino loyihalari qiziqmi?",
    "15. Qishloq xo'jaligi va o'simliklar yetishtirish yoqadimi?",
    "16. Huquq va qonunlarni o'rganish, adolatni himoya qilish qiziqmi?",
    "17. Avtomobillar va texnika mexanizmlari sizni qiziqtiradimi?",
    "18. Maqola yozish, blog yuritish yoki jurnalistikaga qiziqasizmi?",
    "19. Sport va sog'lom turmush tarzini targ'ib qilish yoqadimi?",
    "20. Psixologiya va inson xarakterini o'rganish qiziqmi?",
    "21. Kiberxavfsizlik va axborot himoyasi sohasiga qiziqasizmi?",
    "22. Maktabda dars berish va bilim ulashishni xohlaysizmi?",
    "23. Animatsiya, 3D modellashtirish yoki multfilmlar yaratish yoqadimi?",
    "24. Eksperimentlar o'tkazish va laboratoriya ishlarini yoqtirasizmi?",
    "25. Transport va logistika tizimini boshqarish qiziqmi?",
    "26. Siyosat va davlat boshqaruvi tizimini o'rganish yoqadimi?",
    "27. Marketing va reklama orqali mahsulot sotish qiziqmi?",
    "28. Arxeologiya va tarixiy tadqiqotlar sizni qiziqtiradimi?",
    "29. Dengiz va suv osti dunyosini o'rganishni xohlaysizmi?",
    "30. Ijtimoiy tarmoqlar uchun kreativ kontent yaratish yoqadimi?",
    "31. Robotlar va sun'iy intellekt kelajagiga ishonasizmi?",
    "32. Mehmonxona va turizm sohasida ishlash qiziqmi?",
    "33. Moliyaviy tahlil va bank sohasini yoqtirasizmi?",
    "34. Muhandislik chizmalari va loyihalar bilan ishlash yoqadimi?",
    "35. Sahna san'ati, teatr yoki kinoga qiziqasizmi?",
    "36. Quyosh va shamol energiyasini o'rganish qiziqmi?",
    "37. Ma'lumotlar bazasi (Big Data) bilan ishlash yoqadimi?",
    "38. Oziq-ovqat texnologiyasi va yangi mahsulotlar yaratish qiziqmi?",
    "39. Nanotexnologiyalar va mikroskopik dunyo qiziqmi?",
    "40. Shaxsiy biznes va startap loyihalarni boshlashni xohlaysizmi?"
]

# --- 50 TA ZAMONAVIY KASB RO'YXATI ---
MODERN_JOBS = [
    "1. Data Scientist", "2. Python Developer", "3. UI/UX Designer", "4. Prompt Engineer",
    "5. Cyber Security Expert", "6. Blockchain Developer", "7. Cloud Architect", "8. AI Ethics Specialist",
    "9. Mobile App Developer", "10. Game Developer", "11. DevOps Engineer", "12. Digital Marketer",
    "13. SMM Manager", "14. Content Creator", "15. SEO Specialist", "16. E-commerce Manager",
    "17. Renewable Energy Engineer", "18. Genetic Counselor", "19. Robotics Engineer", "20. Drone Pilot",
    "21. 3D Printing Specialist", "22. Biohacker", "23. Sustainability Consultant", "24. Virtual Reality Designer",
    "25. Augmented Reality Developer", "26. FinTech Analyst", "27. Crypto Trader", "28. Big Data Analyst",
    "29. Growth Hacker", "30. Customer Success Manager", "31. Remote Team Manager", "32. Freelancer",
    "33. Podcaster", "34. Cybersecurity Auditor", "35. Full Stack Developer", "36. Machine Learning Engineer",
    "37. QA Automation Engineer", "38. Product Manager", "39. Business Intelligence Analyst", "40. Copywriter",
    "41. Video Editor (AI based)", "42. Motion Designer", "43. Interior Designer (VR based)", "44. Urban Farmer",
    "45. Telemedicine Doctor", "46. Online Tutor", "47. Digital Transformation Consultant", "48. Influencer",
    "49. Data Privacy Officer", "50. IT Project Manager"
]

# --- ASOSIY MENYU ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Kasbiy so'rovnoma")
    builder.button(text="💡 Kasbiy maslahatlar")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.button(text="📞 Bog'lanish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- SERTIFIKAT ---
def create_modern_cert(name, direction):
    img = Image.new('RGB', (1200, 800), color=(15, 15, 35))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 1160, 760], outline=(0, 255, 255), width=4)
    # Oddiy matn (Render muammosiz chiqishi uchun)
    draw.text((600, 150), "KASBIY YO'NALTIRISH SERTIFIKATI", fill=(0, 255, 255), anchor="mm")
    draw.text((600, 350), name.upper(), fill=(255, 255, 255), anchor="mm")
    draw.text((600, 500), f"Tavsiya: {direction}", fill=(255, 215, 0), anchor="mm")
    path = os.path.join(CERT_FOLDER, f"cert_{datetime.now().timestamp()}.png")
    img.save(path)
    return path

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer(f"Assalomu alaykum, {m.from_user.full_name}!\n'StartUp Maktab' loyihasining rasmiy botiga xush kelibsiz.", reply_markup=main_menu())

@dp.message(F.text == "ℹ️ Maslahatchi haqida")
async def about(m: types.Message):
    info = (
        "👤 **F.I.SH:** Otabek Bakhtiyorovich Botirov\n"
        "🏫 **Lavozimi:** “Kelajak” markazlarining umumiy oʻrta ta’lim muassasalaridagi oʻquvchilar tashabbuslarini qoʻllab-quvvatlash boʻyicha maktab maslahatchisi\n"
        "📍 **Hudud:** Farg'ona viloyati, Rishton tumani\n"
        "📜 **Asos:** Oʻzbekiston Respublikasi MMTV 153–sonli buyrugʻi\n"
        "📸 **Hobbisi:** Foto-video operatorlik, AI kontent yaratish\n"
        "💻 **Raqamli ko'nikma:** Python, aiogram development\n"
        "🚀 **Loyiha:** 'StartUp Maktab' yaratuvchisi\n"
        "🎯 **Maqsad:** Iqtidorli yoshlarni qo'llab-quvvatlash\n"
        "📧 **Aloqa:** @otabekbotirov330\n\n"
        "🌟 **Slogan:** 'Sening bugungi harakating - ertangi natijang!'"
    )
    await m.answer(info)

@dp.message(F.text == "💡 Kasbiy maslahatlar")
async def jobs(m: types.Message):
    text = "🚀 **50 ta zamonaviy va istiqbolli kasblar:**\n\n" + "\n".join(MODERN_JOBS)
    await m.answer(text)

@dp.message(F.text == "📞 Bog'lanish")
async def contact_init(m: types.Message, state: FSMContext):
    await m.answer("Ismingizni va murojaatingizni bitta xabarda yozib qoldiring. Maslahatchi tez orada javob beradi:")
    await state.set_state(ContactState.waiting_message)

@dp.message(ContactState.waiting_message)
async def get_contact(m: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 **Yangi murojaat!**\nKimdan: {m.from_user.full_name}\nID: {m.from_user.id}\nMatn: {m.text}")
    await m.answer("✅ Murojaatingiz yuborildi. Rahmat!")
    await state.clear()

@dp.message(F.text == "📝 Kasbiy so'rovnoma")
async def quiz_init(m: types.Message, state: FSMContext):
    await m.answer("Ism va Familiyangizni kiriting:")
    await state.set_state(QuizState.waiting_name)

@dp.message(QuizState.waiting_name)
async def get_quiz_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text, curr=0, score=0)
    builder = InlineKeyboardBuilder().button(text="Boshlash", callback_data="start_q")
    await m.answer(f"Rahmat, {m.text}. 40 ta savoldan iborat so'rovnomani boshlaymizmi?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "start_q")
async def run_q(c: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder().button(text="Ha", callback_data="v_1").button(text="Yo'q", callback_data="v_0")
    await c.message.edit_text(QUESTIONS[0], reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def process_q(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data['curr'] + 1, data['score'] + int(c.data.split("_")[1])
    
    if curr < len(QUESTIONS):
        await state.update_data(curr=curr, score=score)
        builder = InlineKeyboardBuilder().button(text="Ha", callback_data="v_1").button(text="Yo'q", callback_data="v_0")
        await c.message.edit_text(QUESTIONS[curr], reply_markup=builder.as_markup())
    else:
        # Natija tahlili
        dirs = ["IT va Dasturlash", "Muhandislik", "Tibbiyot", "Ijtimoiy soha", "San'at va Dizayn"]
        res_dir = dirs[score % 5]
        name = data['name']
        await state.clear()
        
        cert = create_modern_cert(name, res_dir)
        
        # Excel
        df = pd.DataFrame([{"Sana": datetime.now(), "Ism": name, "Yo'nalish": res_dir}])
        path = os.path.join(ADMIN_FOLDER, "statistikalar.xlsx")
        if os.path.exists(path):
            df = pd.concat([pd.read_excel(path), df])
        df.to_excel(path, index=False)

        await c.message.delete()
        await bot.send_photo(c.from_user.id, photo=FSInputFile(cert), caption=f"🏁 **So'rovnoma yakunlandi!**\nTavsiya etilgan yo'nalish: **{res_dir}**")
        await bot.send_document(ADMIN_ID, document=FSInputFile(path))

async def main():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
