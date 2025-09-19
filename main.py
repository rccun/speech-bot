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

async def download_data():
    with open('alerts_doc.txt', 'r', encoding='utf-8') as f:
        return f.read()


async def upload_data():
    with open('alerts_doc.txt', 'w', encoding='utf-8') as f:
        for i, j in alerts.items():
            print(f'{i}:{j}')
            f.write(f'{i}:{j}\n')


def convert_toDict(alerts_txt):
    global alerts
    for i in alerts_txt.split('\n'):
        if len(i) != 0:
            alerts[int(i[:i.find(':')])] = int(i[i.find(':') + 1:])
alerts = {}
admins = [1876535694]#1278617806, 1876535694]
group_id = 0
c = 0
usid = 0
usname = ''
k = ''
group_id = -1002970117013
words = ['ебло', 'еблан', 'мудак', 'пидор', 'пидрила', 'захуячу', 'хуета']
shorts = ['бля', 'пизд', 'хуй', 'еба', 'сос', 'хуе']
isLast = False

bot = Bot(token=apiska)
dp = Dispatcher(bot)#, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
@dp.message_handler(commands='start')
async def start(mes: types.Message):
    await bot.send_message("Это бот для фильтрации нецензурных слов в группах. Добавьте меня в группу, выдайте права администратора и я буду удалять сообщения, содержащие нецензурные слова")

@dp.message_handler()
async def filter(mes: types.Message):
    global alerts
    alerts.clear()
    convert_toDict(await download_data())
    print("ID чата", mes.chat.id)
    print("ID пользака", mes.from_user.id)
    
    list_words = mes.text.split()
    #if mes.chat.id != -1002970117013:
    if mes.from_user.id not in admins:
        for k in list_words:
            i = k.lower()
            for j in shorts:
                if i in words or j in i:
                    usname = mes.from_user.username
                    if usname == None:
                        usname = mes.from_user.first_name
                    else: 
                        usname = '@' + mes.from_user.username
                    usid = mes.from_user.id
                    await bot.send_message(group_id, f'в группу {mes.chat.full_name} пидорас {usname} отправил такую хуету: {mes.text}')
                    if usid in alerts.keys():
                        count = (alerts[usid] + 1) % 3
                    else:
                        count = 1
                    alerts[usid] = count
                    if count == 0:
                        until_date = datetime.now() + timedelta(minutes=5)

                        await mes.reply(f'Последнее предупреждение. Бан {usname} на 5 минут')
                        await upload_data()
                        await bot.restrict_chat_member(chat_id=mes.chat.id, user_id=mes.from_user.id, until_date=until_date)
                        await mes.delete()
                        break
                    await bot.send_message(mes.chat.id, f"{usname} Без мата! Мир дружба жвачка\nПредупреждение: {count}/3")
                    await mes.delete()
                    await upload_data()
                    break

    

    
            




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)