import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor

API_TOKEN = '7099011946:AAEiH47rm2TPRt29Dx9P9UdvgUSexe5p8pE'
CHANNEL = '@mamadoctorgonchrovabot'
PDF_FILE = '10_полезных_привычек_для_родителей_нового_поколения_2.pdf'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

check_subscription_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✅ Проверить подписку", callback_data="check_sub")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        f"Чтобы получить доступ к PDF, пожалуйста, подпишитесь на канал: {CHANNEL}\n\n"
        f"После подписки нажмите кнопку ниже 👇",
        reply_markup=check_subscription_kb
    )

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(user_id, "✅ Подписка подтверждена! Отправляю документ…")
            doc = InputFile(PDF_FILE)
            await bot.send_document(user_id, doc)
        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(user_id, f"❌ Вы ещё не подписались на {CHANNEL}. Подпишитесь и нажмите кнопку ещё раз.")
    except Exception as e:
        await bot.send_message(user_id, "🚫 Не удалось проверить подписку. Проверьте, существует ли канал и добавлен ли бот в админы.")
        print(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
