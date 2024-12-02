from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from decouple import config
import requests



router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message):
    token = message.get_args()
    if token:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name

        data = {
            'token': token,
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
        }
        response = requests.post(f'http://{config("URL_APP")}/telegram_auth/', data=data)
        await message.reply('Аутентификация успешна! Вы можете вернуться на сайт.')
    else:
        await message.reply('Токен не найден.')