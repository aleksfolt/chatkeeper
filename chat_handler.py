import json
import asyncio
import aiogram
from aiogram import Bot
from aiogram.types import Message
from time import time, sleep
from calculator import calculate_slow, hui
import datetime

chat = {
    "username": 'hui',
    "prem": "time",
    "chat": "",
    "owner": "pidor",
    "rules": "сосать хуй",
    "admins": {
        "1": 1488,
        "2": 52,
        "3": 228,
        "4": 'svo',
        "5": 'loh'
    },
    "members": 1488,
    "pidors":{
        "nickname": "",
        "who": "",
        "messages": 14888888,
        "when_pass": 52692281488,
        "reputation": 1488,
        "marriage": 1488,
        "clan": 1488,
        "about_yourself": "",
        "vip": 1488,
        "awards": "hui",
        "bookmarks": "",
        "mrp": {}
    },
    "mrp": {},
    "banlist": {},
    "mutelist": {},
    "warnlist": {},
    "clans": {},
    "marriages":{},
    "config": {}
}

awards = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": []
}

async def load_chats():
    with open('chats.json', 'r', encoding='utf8') as f:
        return json.loads(f.read())

async def dump_chats(data):
    with open('chats.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

async def _get_chat_username(message: Message, bot: Bot):
    username = message.chat.username
    if username != None:
        return username
    link = await bot.export_chat_invite_link(message.chat.id)
    return link

async def _get_owner(message: Message, bot: Bot):
    administrators = await bot.get_chat_administrators(message.chat.id)
    owner = next((admin for admin in administrators if admin.status == 'creator'), None)
    return owner


async def _get_members(message: Message, bot: Bot):
    chat = await bot.get_chat(message.chat.id)
    members_count = chat.get("all_members_are_administrators") 
    return members_count

async def check_prem(message: Message, bot: Bot):
    chat = await load_chats()
    if chat[str(message.chat.id)]['prem'] > time():
        return True
    return False

async def _new_chat(message: Message, bot: Bot):
    chat = {
        "username": await _get_chat_username(message, bot),
        "prem": 0,
        "chat": message.chat.title,
        "owner": await _get_owner(message, bot),
        "rules": "Скинь разрабам копеечку и они сделают возможность добавлять правила. (http://t.me/send?start=IVzkR4jd7Z7T)",
        "welcome": "вы лох, привет в чат", 
        "message_count": {},
        "admins": {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [await _get_owner(message, bot)]
        },
        "members": await _get_members(message, bot),
        "pidors":{},
        "mrp": {},
        "banlist": {},
        "mutelist": {},
        "warnlist": {},
        "clans": {},
        "marriages": {},
        "bookmarks": {}, 
        "config": {}
    } 
    data = await load_chats()
    data[str(message.chat.id)]
    await dump_chats(data)

async def _add_member(message: Message, bot: Bot):
    task = await calculate_slow(temperature=0.25, ignore=await check_prem(message, bot))
    sleep(task[0])
    chat = await load_chats()
    data = {
        "nickname": message.from_user.firs_tname,
        "who": "",
        "messages": {},
        "when_pass": time(),
        "reputation": 0,
        "marriage": 0,
        "clan": 0,
        "about_yourself": "",
        "vip": 0,
        "awards": awards, 
        "bookmarks": [],
        "mrp": {}
    }
    chat[str(message.chat.id)][str(message.from_user.id)] = data
    await dump_chats(chat)
    await hui(task)

async def chat_handler(message: Message, bot: Bot):
    task = await calculate_slow(temperature=0.25, ignore=await check_prem(message, bot))
    sleep(task[0])
    
    chat = await load_chats()
    if str(message.chat.id) not in chat:
        await message.reply('сасат, новый чат')
        await _new_chat(message, bot)
    if str(message.from_user.id) not in chat[str(message.chat.id)]['pidors']:
        await message.reply(chat[str(message.chat.id)]['welcome'])
        await _add_member(message, bot)

    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    temp = chat[str(message.chat.id)]['messages']
    if current_date not in temp:
        temp[current_date] = 0
    else:
        temp[current_date] += 1
    chat[str(message.chat.id)]['messages'] = temp
    
    temp = chat[str(message.chat.id)]['pidors']['messages']
    if current_date not in temp:
        temp[current_date] = 0
    else:
        temp[current_date] += 1
    chat[str(message.chat.id)]['pidors']['messages'] = temp
    
    await hui(task)
    


    
    
