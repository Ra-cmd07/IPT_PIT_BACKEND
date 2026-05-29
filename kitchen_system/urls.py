from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from . import views
import os

def debug_env(request):
    return JsonResponse({
        'DJOSER_ACTIVATION_URL': os.environ.get('DJOSER_ACTIVATION_URL', 'NOT SET'),
        'DJANGO_DEBUG': os.environ.get('DJANGO_DEBUG', 'NOT SET'),
    })

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('debug-env/', debug_env),   # ← add this line
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
    path('api/auth/', include('users.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/chatbot/', include('chatbot.urls')),
]