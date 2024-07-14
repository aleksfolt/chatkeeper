import json
import logging
from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import asyncio
from punishments import ban_user, unban_user, mute_user, unmute_user, kick_user, mute_user_2, punishment_handler
from user_control import users_handler, show_profile, change_user_sex, del_user_sex
from chlemini import extract_action_from_response

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

with open('commands.json', 'r', encoding='utf-8') as file:
    com = json.load(file)

async def update_config():
    global config
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    with open('commands.json', 'r', encoding='utf-8') as file:
        com = json.load(file)


API_TOKEN = config['api_key']
LOG_CHAT_ID = config['log_chat_id']  # ID чата, куда будут отправляться логи

# Настройка логирования
logging.basicConfig(level=logging.INFO)



class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self.bot.send_message(chat_id=self.chat_id, text=log_entry))


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Добавляем обработчик логов
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_handler = TelegramLogsHandler(bot, LOG_CHAT_ID)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


async def start_with(message, array):
    for i in array:
        if message.startswith(i):
            return message[(len(i)):]
    return False


async def send_welcome(message: Message):
    await message.reply("Привет! Я асинхронный бот на Python!")
    logging.info(f"User {message.from_user.id} started the bot.")


async def parse_mute_duration(response):
    try:
        parts = response.split()
        if len(parts) == 2 and parts[0] == "mute":
            duration = parts[1]
            unit = duration[-1]
            value = int(duration[:-1])

            if unit == 'h':
                return timedelta(hours=value)
            elif unit == 'm':
                return timedelta(minutes=value)
            elif unit == 'd':
                return timedelta(days=value)
    except (ValueError, IndexError):
        return None

    return None



@dp.message(F.text)
async def echo(message: Message):
    message_lower = message.text.lower()
    await users_handler(message, bot)
    if message_lower in com['start']:
        await send_welcome(message)
    elif message_lower in com['config_update']:
        if message.from_user.id in config['gods']:
            await update_config()
            await message.reply('Конфиг файл успешно обновлен')
        else:
            await message.reply('У вас недостаточно прав для этого действия')
    elif await start_with(message_lower, com['ban']):
        punish = {
            "action": "ban",
            "time": None,
            "id": None,
            "admin": message.from_user.id
        }
        await punishment_handler(await start_with(message_lower, ["/ban", "ban", "/banan", "бан", 'чс']), punish, message, bot)
    elif message_lower in ['/unban', 'unban', 'разбан', 'вернуть', 'back']:
        await unban_user(message, bot)
    elif await start_with(message_lower, ["/mute", 'mute', 'мут']):
        punish = {
            "action": "mute",
            "time": None,
            "id": None,
            "admin": message.from_user.id
        }
        await punishment_handler(await start_with(message_lower, ["/mute", 'mute', 'мут']), punish, message, bot)
    
    elif message_lower in ['/unmute', 'unmute', 'размут', 'анмут']:
        await unmute_user(message, bot)
    elif await start_with(message_lower, ['/kick', 'кик']):
        await kick_user(message, bot)
    elif await start_with(message_lower, ['/profile']):
        await show_profile(message, bot)
    elif await start_with(message_lower, ['/change_sex']):
        await change_user_sex(message, bot)
    elif await start_with(message_lower, ['/del_sex']):
        await del_user_sex(message, bot)

if __name__ == '__main__':
    dp.run_polling(bot)
