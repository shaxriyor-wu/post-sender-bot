import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = "8302327058:AAFk1bDSs5S7VPZLUGfdRHlAaqBAorzJAxk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class KanalStates(StatesGroup):
    kanal = State()
    xabar = State()

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆔 Id yuborish", callback_data="id_yuborish")],
    [InlineKeyboardButton(text="👤 Username yuborish", callback_data="username_yuborish")],
    [InlineKeyboardButton(text="🏢 Bot haqida", callback_data="about")],
])

back_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Ortga", callback_data="back")]
])

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Assalomu alaykum! Kanal ID yoki username yuboring.",
        reply_markup=main
    )

@dp.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Bot orqali kanalga xabar yuborish mumkin. Botni kanalga qo‘shib admin bering.",
        reply_markup=main
    )

@dp.callback_query(F.data == "id_yuborish")
async def id_yuborish(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Kanal ID yuboring (-100 bilan):", reply_markup=back_btn)
    await state.set_state(KanalStates.kanal)

@dp.callback_query(F.data == "username_yuborish")
async def username_yuborish(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Kanal username yuboring (@ bilan):", reply_markup=back_btn)
    await state.set_state(KanalStates.kanal)

@dp.message(KanalStates.kanal)
async def kanal_qabul(message: Message, state: FSMContext):
    await state.update_data(kanal=message.text.strip())
    await message.answer("Endi yubormoqchi bo‘lgan xabaringizni yozing:")
    await state.set_state(KanalStates.xabar)

@dp.message(KanalStates.xabar)
async def xabar_yuborish(message: Message, state: FSMContext):
    data = await state.get_data()
    kanal = data.get("kanal")
    xabar = message.text
    try:
        await bot.send_message(kanal, xabar)
        await message.answer("Xabar kanalga yuborildi.", reply_markup=main)
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    await state.clear()

async def run():
    print("Bot ishga tushdi ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run())
