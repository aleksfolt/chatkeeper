from datetime import datetime, timedelta
from time import time
import json
from aiogram import Bot
from aiogram.types import Message, ChatPermissions
from time_interpritator import time_to_seconds, seconds_to_time

async def _load_users():
    with open('usernames.json', 'r', encoding='utf8') as f:
        return json.loads(f.read())

async def check_blacklist(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['kicked', 'left']  # Проверяем статус пользователя в чате
    except Exception as e:
        print(f"Ошибка при проверке членства пользователя: {e}")
        return False

async def check_is_userid(text):
    for i in range(10):
        if str(i) in text:
            return True
    return False

async def start_with(message, array):
    for i in array:
        if message.startswith(i):
            return True
    return False


async def unban_user(message: Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply("Хуй в нос")
        return
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    if not await check_blacklist(bot, chat_id, user_id):
        await message.reply("Он и так с билетом, иди нахуй")
        return
    try:
        await bot.unban_chat_member(chat_id, user_id)
        await message.reply("С билетом, проходи")
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')


async def _mute_user(message: Message, bot: Bot, punish):
    chat_id = message.chat.id
    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
        )
        if punish['time'] == None:
            await bot.restrict_chat_member(chat_id, punish['id'], permissions)
        else:
            dt = datetime.now() + timedelta(seconds=punish['time'])
            until = dt.timestamp()
            await bot.restrict_chat_member(chat_id, punish['id'], permissions, until_date=until)
        await message.reply("Завали ебало")
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')

async def _ban_user(message: Message, bot: Bot, punish):
    chat_id = message.chat.id
    try:
        await bot.ban_chat_member(chat_id, punish['id'])
        await message.reply("Нет билета, иди нахуй")
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')

async def _kick_user(message: Message, bot: Bot, punish):
    chat_id = message.chat.id

    try:
        if check_blacklist(bot, chat_id, punish['id']):
            await bot.ban_chat_member(chat_id, punish['id'])
            await bot.unban_chat_member(chat_id, punish['id'])
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')

async def _warn_user(message: Message, bot: Bot, punish):
    pass

async def _unmute_user(message: Message, bot: Bot, punish):
    chat_id = message.chat.id
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
        )
        await bot.restrict_chat_member(chat_id, punish['id'], permissions)
        await message.reply("Гавари")
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')

async def _unban_user(message: Message, bot: Bot, punish):
    user_id = punish['id']
    chat_id = message.chat.id
    if not await check_blacklist(bot, chat_id, user_id):
        await message.reply("Он и так с билетом, иди нахуй")
        return
    try:
        await bot.unban_chat_member(chat_id, user_id)
        await message.reply("С билетом, проходи")
    except Exception as e:
        await message.reply(f'Сам иди нахуй, и прихвати с собой {e}')

async def _unwarn_user(message: Message, bot: Bot, punish):
    pass

punish = {
    'action': 'hui',
    'time': 1488,
    'id': 1488,
    'admin': 1488
}

async def _get_id(msg):
    id = ''
    msg = msg.split()
    for i in msg:
        if i.startswith('@'):
            id = i[1:]
            break
    print(id, ' get id') 
    if id == '':
        return None
    if id[0] in '123456789':
        return int(id)
    else:
        users = await _load_users()
        if id in users:
            return int(users[id])
        else:
            return None


async def punishment_handler(msg_low, punish, message: Message, bot: Bot):
    msg_low = msg_low.strip()
    try:
        if message.entities:
            for entity in message.entities:
                if entity.type == "text_mention" and entity.user:
                    user_id = entity.user.id
                    punish['id'] = user_id

        if punish['id'] == None:
            punish['id'] = await _get_id(message.text)
        if punish['id'] == None and message.reply_to_message:
            punish['id'] = message.reply_to_message.from_user.id
        if punish['id'] == None:
            await message.reply("Не удалось найти пользователя")
            return
        if punish.get('action') == 'mute':
            await _mute_user(message, bot, punish)
        elif punish.get('action') == 'ban':
            await _ban_user(message, bot, punish)
        elif punish.get('action') == 'warn':
            await _warn_user(message, bot, punish)
        elif punish.get('action') == 'kick':
            await _kick_user(message, bot, punish)

    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')


async def pardon_handler(msg_low, punish, message: Message, bot: Bot):
    msg_low = msg_low.strip()
    try:
        if message.entities:
            for entity in message.entities:
                if entity.type == "text_mention" and entity.user:
                    user_id = entity.user.id
                    punish['id'] = user_id

        if punish['id'] == None:
            punish['id'] = await _get_id(message.text)
        if punish['id'] == None and message.reply_to_message:
            punish['id'] = message.reply_to_message.from_user.id

        punish['time'] = await time_to_seconds(msg_low)
        print(punish)
        if punish['id'] == None:
            await message.reply("Не удалось найти пользователя")
            return
        if punish.get('action') == 'unmute':
            await _mute_user(message, bot, punish)
        elif punish.get('action') == 'unban':
            await _ban_user(message, bot, punish)
        elif punish.get('action') == 'unwarn':
            await _kick_user(message, bot, punish)
    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')
    
    
        
