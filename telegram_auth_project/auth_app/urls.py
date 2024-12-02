from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='index'),
    path('login/', views.login_view, name='login'),
    path('start_telegram_auth/', views.start_telegram_auth, name='start_telegram_auth'),
    path('telegram_webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('telegram_auth/', views.telegram_auth, name='telegram_auth'),
    path('check_auth/', views.check_auth, name='check_auth'),
    path('logout/', views.logout_view, name='logout'),
]