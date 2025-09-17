apiska = "7750300761:AAEcMj6sPkscdvLTqYJaMap5wYnCYHbbeNw" 
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import BoundFilter
from random import randint
import time
import logging
from datetime import datetime, timedelta
import json

def load_data():
    with open('alerts_doc.json', 'w', encoding='utf-8') as f:
        alerts = json.load(f)
    with open('blacklist.txt', 'w', encoding='utf-8') as f:
        blacklist = f.readline()
alerts = {}
blacklist = []
group_id = 0
c = 0
ids = []
answer = ''
usname = ''
bot = Bot(token=apiska)
dp = Dispatcher(bot)#, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
# @dp.message_handler(commands='start')
# async def start(mes: types.Message):
#    group_id = mes.chat.id
   
#    await mes.answer("Здравствуйте сучки")
    #await bot.send_message(mes.from_user.id,
          #                 'Привет! тут чтото должно быыть написано типа приветствия и рассказа про кафе',
           #                reply_markup=kb)

@dp.message_handler()
async def start(mes: types.Message):
    load_data()
    print(mes.chat.id)
    print(mes.from_user.id)
    group_id = -1002970117013
    words = ['бля', 'блят', 'хуй', 'пизда', 'ебло', 'хуйло', 'еблан', 'хуесос ', 'мудак', 'пидор', 'пидрила', 'заебала', 'захуячу', 'заебашу', 'соси', 'нахуй ', 'похуй']
    shorts = ['бля', 'пизд', 'хуй', 'еба']
    list_words = mes.text.split()
    #if mes.chat.id != -1002970117013:
    #if mes.from_user.id != 1876535694: 
    for i in list_words:
        for j in shorts:
            if i in words or j in i: 
                usname = mes.from_user.username
                if usname in alerts.keys():
                    c = (alerts[usname] + 1) % 3
                else: c = 1
                if c == 0: 
                    await mes.reply(f'Последнее предупреждение. Бан @{usname}')
                    until_date = datetime.now() + timedelta(minutes=2)
                    blacklist.append(usname)
                    await bot.restrict_chat_member(chat_id=mes.chat.id, user_id=mes.from_user.id, until_date=until_date)
                    await mes.delete()
                    break
                alerts[usname] = c
                await mes.reply(f"@{usname} не матерись пжлст\nПредупреждение: {c}/3")
                await bot.send_message(group_id, f'в группу {mes.chat.full_name} пидорас @{usname} отправил такую хуету: {mes.text}')
                await mes.delete()
    # else: 
        #     await mes.reply(f'привет @rccun')
        #     print("ldjfsglkdfjglkfjglsd")









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)