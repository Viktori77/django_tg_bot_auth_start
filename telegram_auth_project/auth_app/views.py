import json
from importlib import import_module
from django.conf import settings
import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from decouple import config
import requests
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import MemoryStorage
from .models import AuthToken


TELEGRAM_BOT_TOKEN = config('TOKEN')
WEBHOOK_URL = f"https://{config('URL_APP')}/telegram_webhook/"

dp = Dispatcher(storage=MemoryStorage())

# Устанавливаем вебхук
response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook",
    data={"url": WEBHOOK_URL}
)

def login_view(request):
    return render(request, 'auth_app/login.html')

def logout_view(request):
    # Получаем текущего пользователя
    user = request.user

    # Если пользователь аутентифицирован, удаляем все его сессии
    if user.is_authenticated:
        # Получаем все сессии пользователя
        sessions = Session.objects.filter(session_key__in=user.session_keys())

        # Удаляем эти сессии
        sessions.delete()
    # Выполняем стандартный выход пользователя
    logout(request)
    
    return redirect('login')

def start_telegram_auth(request):
    token = str(uuid.uuid4())
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    # Save the token and session_key in the database
    AuthToken.objects.create(token=token, session_key=session_key)
    bot_username = config('BOT_USERNAME')
    telegram_url = f'https://t.me/{bot_username}?start={token}'
    return redirect(telegram_url)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            # Process the update manually
            if 'message' in json_data:
                message = json_data['message']
                if 'text' in message and message['text'].startswith('/start'):
                    token = message['text'][6:].strip()  # Remove '/start ' from the message
                    if token:
                        user_id = message['from']['id']
                        username = message['from'].get('username', '')
                        first_name = message['from'].get('first_name', '')

                        data = {
                            'token': token,
                            'user_id': user_id,
                            'username': username,
                            'first_name': first_name,
                        }
                        response = requests.post(f'https://{config("URL_APP")}/telegram_auth/', data=data)
                        # Send a message back to the user
                        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                        chat_id = message['chat']['id']
                        requests.post(send_message_url, data={
                            'chat_id': chat_id,
                            'text': 'Аутентификация успешна! Вы можете вернуться на сайт.'
                        })
                    else:
                        # Handle missing token
                        chat_id = message['chat']['id']
                        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                        requests.post(send_message_url, data={
                            'chat_id': chat_id,
                            'text': 'Токен не найден.'
                        })
        except Exception as e:
            print(f"Error processing update: {e}")
    return HttpResponse('ok')

@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')

        auth_token = AuthToken.objects.filter(token=token).first()

        if auth_token:
            
            session_key = auth_token.session_key

            
            session_engine = import_module(settings.SESSION_ENGINE)
            session = session_engine.SessionStore(session_key)

            
            user, created = User.objects.get_or_create(
                username=f'{username}',
                defaults={'first_name': first_name}
            )

            
            if not created:
                user.first_name = first_name
                user.save()

           
            session['_auth_user_username'] = user.username
            session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
            session.save()

            
            auth_token.is_authenticated = True
            auth_token.username = username
            auth_token.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Invalid token'})
    else:
        return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})

def check_auth(request):
    
    session_key = request.session.session_key

    if session_key:
        try:
            
            auth_tokens = AuthToken.objects.filter(session_key=session_key)

            if auth_tokens.exists():
                auth_token = auth_tokens.last() 
               
                if auth_token.is_authenticated:
                    return JsonResponse({'is_authenticated': True, 'username': auth_token.username})
                else:
                    return JsonResponse({'is_authenticated': False, 'username': None})
            else:
                return JsonResponse({'is_authenticated': False, 'username': None})

        except AuthToken.DoesNotExist:
            pass

    return JsonResponse({'is_authenticated': False, 'username': None})

