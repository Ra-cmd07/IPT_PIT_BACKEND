from rest_framework import serializers
from .models import ChatMessage, ChatFAQ


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user_message', 'bot_response', 'created_at']
        read_only_fields = ['id', 'bot_response', 'created_at']


class ChatFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFAQ
        fields = ['id', 'question', 'answer', 'category']
        read_only_fields = ['id']


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for incoming chat requests"""
    message = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=255, required=False)


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat responses"""
    message = serializers.CharField()
    session_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
