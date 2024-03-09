from celery import Celery
from celery.schedules import crontab
import sys
import asyncio
from settings import *
from aiogram import Bot
from my_db import get_users_with_subs
from wb_request import get_info_from_wb


app = Celery('send_messages', broker='redis://redis:6379/0')

bot = Bot(token=api_token)

async def async_send_message(user):
    try:
        data = get_info_from_wb(user[1])

        text = f"Наименование товара: {data['name']}\n\nЦена: {data['price']/ 100:.2f} Руб 💰\n"\
            f"Рейтинг товара: {data['product_rating']}⭐\nКол-во товаров на складах: {data['quantity_of_product']}📦\n\n"\
            f"Артикул: {data['article']}🏷️"
            
        await bot.send_message(user[0], text)
        print("Sending message...")
    except Exception as ex:
        print(ex)

@app.task
def send_message():
    loop = asyncio.get_event_loop()
    users = get_users_with_subs()
    tasks = [async_send_message(user) for user in users]
    loop.run_until_complete(asyncio.gather(*tasks))


app.conf.beat_schedule = {
    'send-every-5-minutes': {
        'task': 'notifications_sending.send_message',
        'schedule': crontab(minute='*/5'),
    },
}

if __name__ == '__main__':
    app.start()
