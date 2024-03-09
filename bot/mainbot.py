import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from settings import *
from wb_request import get_info_from_wb
from my_db import *


class Get_info_state(StatesGroup):
    first = State()
    second = State()


dp = Dispatcher()


kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить информацию по товару ℹ️"),],
        [KeyboardButton(text="Остановить уведомления 🚫"),],
        [KeyboardButton(text="Получить информацию из БД 📋"),],
    ],
    resize_keyboard=True,
)

ikb_exit = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вернуться 🔙", callback_data=f'exit')]])


@dp.callback_query(F.data =='exit', Get_info_state.first)
async def exit(call, state: FSMContext):
    await state.clear()
    await call.answer("Вы вернулись в меню!")


@dp.callback_query(F.data.contains('subscribe'))
async def subscribe(call):
    if add_user_sub(user_id=call.message.chat.id, article=call.data.split("_")[-1]):
        await call.answer("Вы успешно подписались!")
    else:
        await call.answer("Кажется вы уже подписаны на этот товар")

@dp.message(CommandStart())
async def start(message):
    await message.answer("Добрый день! Чем могу помочь?", reply_markup=kb_menu)


@dp.message(Get_info_state.first)
async def get_info(message, state: FSMContext):
    if data := get_info_from_wb(message.text):

        ikb_add_sub = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
            text="Подписаться ✅", callback_data=f'subscribe_{data["article"]}')]])

        await message.answer(f"Наименование товара: {data['name']}\n\nЦена: {data['price']/ 100:.2f} Руб 💰\n"\
                             f"Рейтинг товара: {data['product_rating']}⭐\nКол-во товаров на складах: {data['quantity_of_product']}📦\n\n"\
                             f"Артикул: {data['article']}🏷️", reply_markup=ikb_add_sub)
        await state.clear()
    else:
        await message.answer("Товаров по данному артикулу не найдено, попробуйте ввести другой артикул", reply_markup=ikb_exit)


@dp.message()
async def menu(message, state: FSMContext):
    if message.text == "Получить информацию по товару ℹ️":
        await state.set_state(Get_info_state.first)
        await message.answer("Введите артикул товара", reply_markup=ikb_exit)

    elif message.text == "Остановить уведомления 🚫":
        del_user_subs(user_id=message.chat.id)
        await message.answer("Вы отключили все уведомления")

    elif message.text == "Получить информацию из БД 📋":
        data = get_5last(user_id=message.chat.id)
        c = "\n"
        await message.answer("Ваши последние подписки:\n" + ''.join([f"- {article[0]} {article[1].strftime('%Y-%m-%d %H:%M:%S')} {c}\n" for article in data]))



async def main():
    bot = Bot(token=api_token)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
