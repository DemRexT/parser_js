from aiogram import Bot, Dispatcher, types, executor
from parser_js import main

import datetime


import logging

TOKEN = '7156542758:AAFBxsyC6-JJv4PrZLpy7LPtAhQqcntQcbY'

bot = Bot(TOKEN)
dp = Dispatcher(bot)



logging.basicConfig(level=logging.INFO)
# logging.info("вывод в консоль")

current_date = datetime.datetime.now().strftime('%m-%d')



@dp.message_handler(commands = "start")
async def start_command(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Подождите...')
    main()
    await message.answer_document(open(f'magnit_{current_date}.csv', "rb"))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)