from aiogram import Bot
from aiogram.types import Message
import aiofiles
import json
import os
import time


async def get_user_data():
    if not os.path.exists('users.json'):
        return {}
    async with aiofiles.open('users.json', 'r', encoding='utf-8') as file:
        try:
            return json.loads(await file.read())
        except json.JSONDecodeError:
            return {}


async def dump_user_data(data):
    async with aiofiles.open('users.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))


async def get_usernames():
    if not os.path.exists('usernames.json'):
        return {}
    async with aiofiles.open('usernames.json', 'r', encoding='utf-8') as file:
        try:
            return json.loads(await file.read())
        except json.JSONDecodeError:
            return {}


async def dump_usernames(data):
    async with aiofiles.open('usernames.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))


async def check_int(line):
    for i in line:
        if i not in ['1234567890']:
            return False
    return True



async def set_age(message: Message, bot: Bot):
    data = await get_user_data()
    user_id = str(message.from_user.id)
    if len(message.text.split()) == 2:
        age = message.text.split()[1]
        if check_int(age):
            data[user_id]['age'] = age
            await dump_user_data(data)
            await message.reply('Возраст успешно изменен')
        else:
            await message.reply('Некорректный аргумент')


async def del_age(message: Message, bot: Bot):
    data = await get_user_data()
    user_id = str(message.from_user.id)
    data[user_id]['age'] = 'Не указано'
    await dump_user_data(data)
    await message.reply('Возраст успешно удален')



async def change_user_sex(message: Message, bot: Bot):
    data = await get_user_data()
    user_id = str(message.from_user.id)
    sex = message.text.split()
    if len(sex) == 2:
        sex = sex[1]
        if sex in ['m', 'male', 'м', 'мужской']:
            data[user_id]['sex'] = 'мужской'
            await message.reply('Пол изменен')
        elif sex in ['f', 'female', 'w', 'woman', 'вуман', 'ж', 'женский']:
            data[user_id]['sex'] = 'женский'
            await message.reply('Пол изменен')
        elif sex in ['other', 'др', 'другой']:
            data[user_id]['sex'] = 'другой'
            await message.reply('Пол изменен')
        else:
            await message.reply('Некорректный аргумент')
    await dump_user_data(data)


async def del_user_sex(message: Message, bot: Bot):
    data = get_user_data()
    user_id = str(message.from_user.id)
    data[user_id]['sex'] = 'Не указано'
    await dump_user_data(data)


async def show_profile(message: Message, bot: Bot):
    users_data = await get_user_data()
    user_id = str(message.from_user.id)

    if user_id not in users_data:
        await message.reply("Такого пользователя не существует")
        return

    data = users_data[user_id]
    await message.reply(f"Имя: {data['firstname']}\n\n"
                        f"user id: {user_id}\n"
                        f"Количество сообщений: {data['total_message_count']}\n"
                        f"Пол: {data['sex']}")


async def users_handler(message: Message, bot: Bot):
    user = message.from_user
    user_id = str(user.id)
    users_data = await get_user_data()
    usernames = await get_usernames()

    if user_id not in users_data:
        users_data[user_id] = {
            "username": user.username,
            "firstname": user.first_name,
            "total_message_count": 0,
            "system_ban": 0,
            "sex": 'Не указан',
            "age": 'Не указан',
            "city": 'Не указан',
            "registration_time": time.time()
        }
        usernames[user.username] = user.id

    if user.username != users_data[user_id]['username']:
        if users_data[user_id]['username'] in usernames:
            del usernames[users_data[user_id]['username']]
        if user.username:
            usernames[user.username] = user_id
        users_data[user_id]['username'] = user.username

    await dump_usernames(usernames)
    await dump_user_data(users_data)
    
