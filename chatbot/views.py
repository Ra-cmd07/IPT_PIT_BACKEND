import os
import traceback
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import ChatMessage, ChatFAQ
from .serializers import (
    ChatMessageSerializer, ChatFAQSerializer,
    ChatRequestSerializer, ChatResponseSerializer
)


class ChatbotAPIView(APIView):
    """Main chatbot endpoint for handling customer messages"""
    
    def post(self, request):
        """
        Handle incoming chat messages
        Expected payload: {
            "message": "user message",
            "session_id": "optional-session-id"
        }
        """
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())
        
        # Get bot response
        bot_response = self._get_bot_response(message, session_id)
        
        # Save chat message
        chat_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id,
            user_message=message,
            bot_response=bot_response
        )
        
        return Response({
            'message': bot_response,
            'session_id': session_id,
            'timestamp': chat_msg.created_at
        }, status=status.HTTP_200_OK)
    
    def _get_bot_response(self, user_message, session_id):
        """
        Generate bot response using OpenAI API
        Falls back to FAQ/template responses if API not configured
        """
        try:
            return self._get_openai_response(user_message, session_id)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            traceback.print_exc()
            return self._get_fallback_response(user_message)
    
    def _get_openai_response(self, user_message, session_id):
        """Call OpenAI API for intelligent responses"""
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        # Get chat history for context
        history = self._get_chat_history(session_id)
        
        # Get relevant FAQs
        faqs = self._get_relevant_faqs(user_message)
        
        system_prompt = f"""You are a helpful customer support assistant for a kitchen/restaurant ordering system. 
You help customers with:
- Order tracking and status
- Billing and payment questions
- Technical issues with the platform
- General restaurant information and FAQs

Be friendly, professional, and concise. If you don't know something, offer to escalate to a human agent.

RELEVANT FAQs:
{self._format_faqs(faqs)}"""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in history[-6:]:  # Last 3 exchanges to avoid token limits
            messages.append({"role": "user", "content": msg['user_message']})
            messages.append({"role": "assistant", "content": msg['bot_response']})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Using Google Gemini 3.5 (Latest Free Tier) with the OpenAI library
        gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
        gemini_model = "gemini-3.5-flash"

        if hasattr(openai, 'OpenAI'):
            client = openai.OpenAI(api_key=api_key, base_url=gemini_base_url)
            response = client.chat.completions.create(
                model=gemini_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            openai.api_key = api_key
            openai.api_base = gemini_base_url
            response = openai.ChatCompletion.create(
                model=gemini_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
    
    def _get_fallback_response(self, user_message):
        """Fallback response using FAQ matching"""
        faqs = self._get_relevant_faqs(user_message)
        
        if faqs:
            faq = faqs[0]
            return f"Based on our FAQs: {faq.answer}\n\nFor more help, please contact our support team."
        
        return """Thank you for your message! I'm learning to respond better. 
        
For immediate assistance, please contact our support team or check our FAQ section. 
How can I help you today? I can assist with:
- Order tracking
- Billing questions
- Technical issues
- Restaurant information"""
    
    def _get_relevant_faqs(self, query):
        """Find relevant FAQs based on user query"""
        stop_words = {'how', 'do', 'i', 'what', 'is', 'the', 'a', 'to', 'can', 'you', 'my', 'in', 'for', 'of', 'are'}
        keywords = [kw for kw in query.lower().split() if kw not in stop_words]
        faqs = ChatFAQ.objects.filter(active=True)
        
        results = []
        for faq in faqs:
            score = sum(1 for kw in keywords if kw in faq.question.lower() or kw in faq.answer.lower())
            if score > 0:
                results.append((faq, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [faq for faq, score in results[:3]]
    
    def _get_chat_history(self, session_id):
        """Get chat history for a session"""
        return list(
            ChatMessage.objects.filter(session_id=session_id)
            .values('user_message', 'bot_response')
            .order_by('created_at')
        )
    
    def _format_faqs(self, faqs):
        """Format FAQs for the system prompt"""
        if not faqs:
            return "No relevant FAQs found."
        return "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])


class ChatHistoryViewSet(viewsets.ModelViewSet):
    """View chat history"""
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ChatMessage.objects.filter(user=self.request.user)
        
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return ChatMessage.objects.filter(session_id=session_id)
        
        return ChatMessage.objects.none()


class ChatFAQViewSet(viewsets.ModelViewSet):
    """Manage FAQs for the chatbot"""
    queryset = ChatFAQ.objects.filter(active=True)
    serializer_class = ChatFAQSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get FAQs by category"""
        category = request.query_params.get('category')
        if category:
            faqs = ChatFAQ.objects.filter(active=True, category=category)
        else:
            faqs = ChatFAQ.objects.filter(active=True)
        
        serializer = self.get_serializer(faqs, many=True)
        return Response(serializer.data)
