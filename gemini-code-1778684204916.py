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
TOKEN = "7919823792:AAEj9P..." # O'z tokeningizni qo'ying
ADMIN_ID = 8323916383 
ADMIN_FOLDER, CERT_FOLDER = "admin_data", "certificates"
EXCEL_FILE = os.path.join(ADMIN_FOLDER, "umumiy_natijalar.xlsx")

for f in [ADMIN_FOLDER, CERT_FOLDER]:
    if not os.path.exists(f): os.makedirs(f)

logging.basicConfig(level=logging.INFO)
bot, dp = Bot(token=TOKEN), Dispatcher()

class QuizState(StatesGroup):
    waiting_name = State()
    answering = State()

class ContactState(StatesGroup):
    waiting_message = State()

# --- 40 TA SAVOL ---
QUESTIONS = [f"{i}-savol. Tanlagan yo'nalishingiz bo'yicha innovatsion loyihalar yaratishni xohlaysizmi?" for i in range(1, 41)]

# --- 50 TA ZAMONAVIY KASB ---
MODERN_JOBS = [f"{i}. Zamonaviy kasb nomi" for i in range(1, 51)] # Buni yuqoridagi ro'yxat bilan to'ldirishingiz mumkin

# --- SERTIFIKAT YARATISH (SHABLON ASOSIDA) ---
def create_final_certificate(full_name, direction):
    # Siz yuklagan 'template.png' rasmidan foydalanamiz
    template_path = "template.png"
    if not os.path.exists(template_path):
        # Agar shablon bo'lmasa, vaqtinchalik fon yaratadi
        img = Image.new('RGB', (1200, 900), color=(10, 20, 40))
    else:
        img = Image.open(template_path)
    
    draw = ImageDraw.Draw(img)
    
    # Renderda ishlaydigan standart shrift
    try:
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_info = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        font_name = font_info = ImageFont.load_default()

    # Ismni rasmning markaziga yozish (Koordinatalarni templatega qarab moslang)
    # Taxminiy koordinata: (600, 450) - ism uchun
    draw.text((600, 460), full_name.upper(), fill=(255, 255, 255), font=font_name, anchor="mm")
    
    # Yo'nalish va natija
    draw.text((600, 580), f"Yo'nalish: {direction}", fill=(200, 200, 200), font=font_info, anchor="mm")
    draw.text((800, 750), datetime.now().strftime("%d.%m.%Y"), fill=(255, 255, 255), font=font_info)

    path = os.path.join(CERT_FOLDER, f"cert_{datetime.now().timestamp()}.png")
    img.save(path)
    return path

# --- EXCELNI YANGILASH ---
def update_excel(name, user_id, direction):
    new_data = {
        "Sana": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "F.I.SH": [name],
        "Telegram ID": [user_id],
        "Tavsiya etilgan yo'nalish": [direction]
    }
    df_new = pd.DataFrame(new_data)
    
    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
        
    df_final.to_excel(EXCEL_FILE, index=False)
    return EXCEL_FILE

# --- ASOSIY HANDLERLAR ---
@dp.message(Command("start"))
async def start(m: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Kasbiy so'rovnoma")
    builder.button(text="💡 Kasbiy maslahatlar")
    builder.button(text="ℹ️ Maslahatchi haqida")
    builder.button(text="📞 Bog'lanish")
    builder.adjust(2)
    await m.answer(f"Assalomu alaykum! 'StartUp Maktab' botiga xush kelibsiz.", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "ℹ️ Maslahatchi haqida")
async def about(m: types.Message):
    info = (
        "👤 **F.I.SH:** Otabek Bakhtiyorovich Botirov\n"
        "🏫 **Lavozimi:** Maktab maslahatchisi\n"
        "📍 **Hudud:** Rishton tumani\n"
        "🚀 **Loyiha:** 'StartUp Maktab' va @tashabbus_maktab_bot yaratuvchisi\n"
        "🎯 **Maqsad:** Iqtidorli yoshlarni kashf qilish."
    )
    await m.answer(info)

@dp.message(F.text == "📝 Kasbiy so'rovnoma")
async def quiz_init(m: types.Message, state: FSMContext):
    await m.answer("Ism va Familiyangizni kiriting:")
    await state.set_state(QuizState.waiting_name)

@dp.message(QuizState.waiting_name)
async def get_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text, curr=0, score=0)
    builder = InlineKeyboardBuilder().button(text="🚀 Boshlash", callback_data="start_q")
    await m.answer(f"Rahmat, {m.text}. So'rovnomani boshlaymizmi?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "start_q")
async def run_q(c: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="v_1").button(text="❌ Yo'q", callback_data="v_0")
    await c.message.edit_text(f"1-savol: {QUESTIONS[0]}", reply_markup=builder.as_markup())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def process_q(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curr, score = data['curr'] + 1, data['score'] + int(c.data.split("_")[1])
    
    if curr < len(QUESTIONS):
        await state.update_data(curr=curr, score=score)
        builder = InlineKeyboardBuilder().button(text="✅ Ha", callback_data="v_1").button(text="❌ Yo'q", callback_data="v_0")
        await c.message.edit_text(f"{curr+1}-savol: {QUESTIONS[curr]}", reply_markup=builder.as_markup())
    else:
        # Natijani hisoblash
        dirs = ["IT SOHASI", "MUHANDISLIK", "TIBBIYOT", "GUMANITAR", "SAN'AT VA DIZAYN"]
        res_dir = dirs[score % 5]
        name = data['name']
        await state.clear()
        
        # 1. Excelni yangilash
        excel_path = update_excel(name, c.from_user.id, res_dir)
        
        # 2. Sertifikat yaratish
        cert_path = create_final_certificate(name, res_dir)
        
        await c.message.delete()
        await bot.send_photo(c.from_user.id, photo=FSInputFile(cert_path), 
                             caption=f"🏁 **So'rovnoma yakunlandi!**\n\nSizga **{res_dir}** yo'nalishi tavsiya etiladi. Sertifikatni yuklab oling!")
        
        # 3. Adminga umumiy bazani yuborish
        await bot.send_message(ADMIN_ID, f"📊 Yangi natija: {name} ({res_dir})")
        await bot.send_document(ADMIN_ID, document=FSInputFile(excel_path), caption="📁 Umumiy natijalar bazasi (Excel)")

async def main():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())