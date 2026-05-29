from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """Store chat messages for history and analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, db_index=True)  # For anonymous users
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', '-created_at']),
        ]
    
    def __str__(self):
        return f"Chat {self.session_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ChatFAQ(models.Model):
    """Knowledge base for FAQ to enhance chatbot responses"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('orders', 'Orders'),
            ('billing', 'Billing'),
            ('technical', 'Technical'),
            ('restaurant', 'Restaurant'),
            ('general', 'General'),
        ]
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'question']
    
    def __str__(self):
        return f"{self.category} - {self.question}"
