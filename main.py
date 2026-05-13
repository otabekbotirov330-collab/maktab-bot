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
TOKEN = "7919823792:AAHD8CtrfxeGOPm0m6fZ8YcJzHODvwReKR4"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class QuizState(StatesGroup):
    answering = State()

class SupportState(StatesGroup):
    waiting_for_msg = State()

# --- 40 TA PROFESSIONAL SAVOL ---
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
    return web.Response(text="Metodik tizim faol!")

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Kasb tanlash")
    builder.button(text="👨‍👩‍👧‍👦 Ota-onalar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.button(text="📚 Foydali linklar")
    builder.button(text="📞 Maslahatchi bilan bog'lanish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- HANDLERLAR ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"🌟 Salom {message.from_user.first_name}! Men **Maktab maslahatchisi** botiman. Bo'limlardan birini tanlang:", reply_markup=main_menu())

@dp.message(F.text == "🔍 Kasb tanlash")
async def career_section(message: types.Message):
    tips = [
        "1. IKIGAI metodidan foydalaning.", "2. Kelajak kasblari reytingini kuzating.",
        "3. IT sohasida faqat dasturlash emas, tahlil ham muhim.", "4. Soft Skills har doim birinchi o'rinda.",
        "5. Tanlagan sohangizda mentor toping.", "6. Chet tilini o'rganishni kechiktirmang.",
        "7. Tanqidiy fikrlashni rivojlantiring.", "8. Kasbning qiyin tomonlarini ham o'rganing.",
        "9. O'z qiziqishlaringizni kundalikka yozib boring.", "10. Stajyorlik dasturlarida qatnashing.",
        "11. Networking (tanish-bilish) bazasini yarating.", "12. Sun'iy intellekt bilan ishlashni o'rganing.",
        "13. Moliyaviy savodxonlikni oshiring.", "14. Ommaviy nutq so'zlashni mashq qiling.",
        "15. Portfolio yaratishni hozirdan boshlang.", "16. SMM va raqamli marketingni o'rganing.",
        "17. Tadbirkorlik ko'nikmalarini egallang.", "18. Stressli vaziyatlarda ishlashni o'rganing.",
        "19. Vaqtni boshqarish (Time management).", "20. Jamoada ishlash madaniyatini shakllantiring.",
        "21. Turli sohalar chorrahasidagi kasblarni ko'ring.", "22. Psixologik testlardan o'tib turing.",
        "23. Bozor talabini doimiy tahlil qiling.", "24. Texnik bilimlarni chuqurlashtiring.",
        "25. Kreativ yondashuvni shakllantiring.", "26. Maqsadni aniq qo'ying (SMART).",
        "27. O'z ustingizda ishlashdan to'xtamang.", "28. Har bir xatoni tajriba deb biling.",
        "29. Dunyoqarashingizni kengaytiring.", "30. O'z sohangizdagi yangiliklarni o'qing."
    ]
    await message.answer("🎯 **Kasb tanlash bo'yicha 30 ta tavsiya:**\n\n" + "\n".join(tips))

@dp.message(F.text == "👨‍👩‍👧‍👦 Ota-onalar uchun")
async def parents_section(message: types.Message):
    tips = [
        "1. Farzandingizni boshqalar bilan solishtirmang.", "2. Uning qiziqishlarini qo'llab-quvvatlang.",
        "3. O'zingiz orzu qilgan kasbga uni majburlamang.", "4. Farzand bilan do'stona muloqot o'rnating.",
        "5. Uning har bir yutug'ini e'tirof eting.", "6. Xato qilishiga imkon bering.",
        "7. Zamonaviy ta'lim tizimini o'rganing.", "8. Bola bilan birga kelajakni rejalashtiring.",
        "9. Uyda xotirjam muhit yarating.", "10. Farzandning ruhiy holatiga e'tibor bering.",
        "11. Uning hobbilariga sarmoya kiriting.", "12. Kasb tanlashda maslahatchi bilan gaplashing.",
        "13. OTMlar haqida birga ma'lumot qidiring.", "14. Farzandingizga o'rnak bo'ling.",
        "15. Uning mustaqil qarorlarini hurmat qiling.", "16. Texnologiyadan to'g'ri foydalanishni o'rgating.",
        "17. Sport va sog'lom turmush tarzini targ'ib qiling.", "18. Farzandning iste'dodini barvaqt aniqlang.",
        "19. Unga motivatsiya beruvchi kitoblar oling.", "20. Sabrli bo'lishni o'rganing va o'rgating.",
        "21. Bolaning mantiqiy fikrlashini oshiring.", "22. Chet tili kurslariga yo'naltiring.",
        "23. Ijtimoiy tarmoqlar ta'sirini nazorat qiling.", "24. Farzandingizga vaqt ajrating.",
        "25. Uning qobiliyatini kashf qilishiga yordam bering.", "26. Moliyaviy tarbiya bering.",
        "27. Farzandning orzularini masxara qilmang.", "28. Uyda kichik loyihalar topshiring.",
        "29. Kelajak texnologiyalaridan xabardor bo'ling.", "30. Farzandingizga doimo ishonishingizni ayting."
    ]
    await message.answer("👨‍👩‍👧‍👦 **Ota-onalar uchun 30 ta metodik tavsiya:**\n\n" + "\n".join(tips))

@dp.message(F.text == "👨‍🏫 O'qituvchilar uchun")
async def teachers_section(message: types.Message):
    tips = [
        "1. Darsni qiziqarli hikoya bilan boshlang.", "2. Interaktiv o'yinlardan foydalaning.",
        "3. O'quvchilarning har bir savoliga javob bering.", "4. Raqamli doska va infografikadan foydalaning.",
        "5. Har bir o'quvchining kuchli tomonini toping.", "6. Darsda tanqidiy tahlilga o'rin bering.",
        "7. O'quvchilarni loyiha asosida o'qiting.", "8. Xato qilgan o'quvchini kamsitmang.",
        "9. Dars o'rtasida qisqa tanaffus qiling.", "10. Yangi pedagogik metodlarni o'rganing.",
        "11. Mentorlik qobiliyatingizni oshiring.", "12. O'quvchilar bilan samimiy bo'ling.",
        "13. Motivatsion videolar ko'rsating.", "14. Darsda jamoaviy ishlashni targ'ib qiling.",
        "15. Bilimni amaliyot bilan bog'lang.", "16. O'quvchilarni ijodkorlikka undang.",
        "17. ChatGPT va AI bilan ishlashni o'rgating.", "18. Ota-onalar bilan yaqin aloqada bo'ling.",
        "19. O'z ustingizda doimiy ishlang.", "20. Stressga chidamlilikni oshiring.",
        "21. Darsda vaqtni to'g'ri taqsimlang.", "22. O'quvchilarning ruhiy holatini his qiling.",
        "23. Har bir darsga yangilik olib kiring.", "24. Sahnada nutq so'zlash mahoratini o'rgating.",
        "25. O'quvchilarni mustaqil bilim olishga undang.", "26. Bilimlarni hayotiy misollar bilan tushuntiring.",
        "27. Zamonaviy baholash tizimini joriy qiling.", "28. Metodik qo'llanmalarni doimiy yangilang.",
        "29. O'quvchilarga ishonch bildiring.", "30. Pedagoglik kasbini seving!"
    ]
    await message.answer("👨‍🏫 **O'qituvchilar uchun 30 ta metodik yordam:**\n\n" + "\n".join(tips))

@dp.message(F.text == "ℹ️ Maslahatchi haqida")
async def counselor_info(message: types.Message):
    info = [
        "👤 **F.I.SH:** Otabek Bakhtiyorovich Botirov",
        "🏫 **Lavozimi:** “Kelajak” markazlarining umumiy oʻrta ta’lim muassasalaridagi oʻquvchilar tashabbuslarini qoʻllab-quvvatlash boʻyicha maktab maslahatchisi",
        "📍 **Hudud:** Farg'ona viloyati, Rishton tumani",
        "📜 **Asos:** Oʻzbekiston Respublikasi Maktabgacha va maktab ta’limi vazirining 2026-yil “21”-apreldagi 153–sonli buyrugʻiga ILOVA",
        "📸 **Hobbisi:** Foto-video operatorlik, sun'iy intellekt yordamida kontent yaratish",
        "💻 **Raqamli ko'nikma:** Python, aiogram bot development, raqamli marketing",
        "🚀 **Loyiha:** 'StartUp Maktab' va @tashabbus_maktab_bot yaratuvchisi",
        "🎯 **Maqsad:** Iqtidorli yoshlarni 'Presidential Gifted Children' dasturiga tayyorlash",
        "🛠 **Asosiy yo'nalishi:** O'quvchilar tashabbuslari va loyihalarini koordinatsiya qilish",
        "📖 **Faoliyat:** 'Yosh kitobxon' ko'rik tanlovi koordinatori",
        "🏛 **Hamkorlik:** 'Kelajak' markazi va School No. 6 o'rtasidagi koordinator",
        "💼 **Ish uslubi:** Innovatsion loyihalar va STARTUP tashabbuslarini qo'llash",
        "📅 **Qabul:** Doimiy ravishda Telegram orqali ochiq muloqotda",
        "📧 **Aloqa:** @otabekbotirov330",
        "🔎 **Tahlil:** Har bir o'quvchining ichki potensialini kashf qilish",
        "📈 **Natija:** Yuzlab o'quvchilarga to'g'ri yo'l ko'rsatish",
        "🤖 **Bot:** Ushbu tizim o'quvchilar va ustozlar uchun begaraz yaratildi.",
        "📊 **Tajriba:** STEM va raqamli texnologiyalar integratsiyasi bo'yicha mutaxassis.",
        "🌟 **Slogan:** 'Sening bugungi harakating - ertangi natijang!'",
        "🕊 **Shior:** 'Yoshlar - yurt kelajagi, ularga yo'l ko'rsatish bizning burchimiz!'"
    ]
    await message.answer("ℹ️ **Maktab maslahatchisi haqida batafsil:**\n\n" + "\n".join(info))

@dp.message(F.text == "📚 Foydali linklar")
async def links_section(message: types.Message):
    text = ("📚 **Foydali manbalar (10 tadan ortiq):**\n\n"
            "🛠 **Kasb-hunar o'rganish:**\n"
            "• [Kasbim.uz](http://kasbim.uz) — Kasblar portal.\n"
            "• [Ish.uz](https://ish.uz) — Bo'sh ish o'rinlari.\n"
            "• [My.mehnat.uz](https://my.mehnat.uz) — Bandlik bazasi.\n"
            "• [It-park.uz](https://it-park.uz) — IT ta'limi.\n\n"
            "🎓 **OTMlar va Grantlar:**\n"
            "• [Uzbmb.uz](https://my.uzbmb.uz) — DTM testlari.\n"
            "• [Edu.uz](https://edu.uz) — OTM yangiliklari.\n"
            "• [Studyin.uz](https://studyinuzbekistan.uz) — Institutlar.\n"
            "• [Grantlar.uz](https://grantlar.uz) — Bepul grantlar.\n\n"
            "📖 **Ustozlar uchun qo'llanmalar:**\n"
            "• [Ziyonet.uz](http://ziyonet.uz) — Ta'lim portali.\n"
            "• [Kitob.uz](https://kitob.uz) — Elektron darsliklar.\n"
            "• [Metodik.uz](http://metodik.uz) — Dars ishlanmalari.\n"
            "• [KhanAcademy](https://uz.khanacademy.org) — Jahon darslari.")
    await message.answer(text, disable_web_page_preview=True)

@dp.message(F.text == "📞 Maslahatchi bilan bog'lanish")
async def support_start(message: types.Message, state: FSMContext):
    await message.answer("✍️ Savolingizni yozib qoldiring. Maslahatchi tez orada javob beradi:")
    await state.set_state(SupportState.waiting_for_msg)

@dp.message(SupportState.waiting_for_msg)
async def support_done(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 **Yangi murojaat!**\n👤: {message.from_user.full_name}\n✍️: {message.text}")
    await message.answer("✅ Xabaringiz yuborildi. Rahmat!")
    await state.clear()

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_start(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data="q_1")
    builder.button(text="❌ Yo'q", callback_data="q_0")
    await message.answer("📝 **Professional test (40 ta savol)**\n\n" + QUESTIONS[0], reply_markup=builder.as_markup())
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
        res = "🌟 Yuqori salohiyat! Tahliliy sohalarga moyilsiz." if score > 30 else "💡 Ijodiy va ijtimoiy sohalarda muvaffaqiyat qozonasiz."
        await callback.message.edit_text(f"🏁 Test tugadi!\nNatija: {score}/40 ball.\n\n{res}")
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
