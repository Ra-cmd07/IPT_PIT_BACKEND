from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatbotAPIView, ChatHistoryViewSet, ChatFAQViewSet

router = DefaultRouter()
router.register(r'history', ChatHistoryViewSet, basename='chat-history')
router.register(r'faqs', ChatFAQViewSet, basename='chat-faq')

urlpatterns = [
    path('', ChatbotAPIView.as_view(), name='chatbot'),
    path('', include(router.urls)),
]
