from django.contrib import admin
from .models import ChatMessage, ChatFAQ


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['session_id', 'user_message', 'bot_response']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ChatFAQ)
class ChatFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'active', 'created_at']
    list_filter = ['category', 'active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at']
    ordering = ['category', 'question']
