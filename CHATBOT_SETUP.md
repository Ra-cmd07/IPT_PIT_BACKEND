# Customer Support AI Chatbot

A full-featured AI-powered customer support chatbot integrated into your Django/React kitchen management system.

## Features

✅ **AI-Powered Responses** - Uses OpenAI's GPT-3.5-turbo for intelligent conversations
✅ **Session Management** - Tracks conversations per user/session
✅ **FAQ Knowledge Base** - Built-in FAQ system to enhance responses
✅ **Chat History** - Stores conversation history for analytics
✅ **Context-Aware** - Uses conversation history for better responses
✅ **Fallback Support** - Works without OpenAI API using FAQ matching
✅ **React Chat UI** - Beautiful floating chat widget for frontend
✅ **Admin Panel** - Manage FAQs and view conversations

## Setup Instructions

### 1. Backend Setup

#### Install OpenAI Package
```bash
pip install openai
```

#### Set Environment Variable
Create a `.env` file in your project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it in your system environment variables.

#### Run Migrations
```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

#### Create Initial FAQs (Optional)
```bash
python manage.py shell
```

Then in the Python shell:
```python
from chatbot.models import ChatFAQ

ChatFAQ.objects.create(
    question="How do I track my order?",
    answer="You can track your order in the 'My Orders' section. Click on any order to see the current status and estimated delivery time.",
    category="orders"
)

ChatFAQ.objects.create(
    question="What payment methods do you accept?",
    answer="We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and digital wallets.",
    category="billing"
)

ChatFAQ.objects.create(
    question="How do I report a technical issue?",
    answer="You can report technical issues through our support chat or email support@kitchen-system.com with details about the problem.",
    category="technical"
)

exit()
```

### 2. Frontend Setup

#### Install UUID Package
```bash
npm install uuid
```

#### Add Chat Component to Your App
In your main app component (e.g., `src/App.tsx`):

```tsx
import CustomerSupportChat from './components/CustomerSupportChat';

function App() {
  return (
    <div>
      {/* Your existing app content */}
      <CustomerSupportChat />
    </div>
  );
}

export default App;
```

#### Configure API URL
In your `.env.local` or environment file:
```
VITE_API_BASE=http://localhost:8000
```

### 3. Test the Chatbot

1. Start your Django backend:
   ```bash
   python manage.py runserver 8000
   ```

2. Start your React frontend:
   ```bash
   npm run dev
   ```

3. Open the chat widget by clicking the floating button in the bottom-right corner

## API Endpoints

### Send Chat Message
**POST** `/api/chatbot/`

Request:
```json
{
  "message": "How do I track my order?",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "message": "Bot response here...",
  "session_id": "session-uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Chat History
**GET** `/api/chatbot/history/?session_id=session-uuid`

### View FAQs
**GET** `/api/chatbot/faqs/`
**GET** `/api/chatbot/faqs/by_category/?category=orders`

### Manage FAQs (Admin)
**POST** `/api/chatbot/faqs/`
**PUT** `/api/chatbot/faqs/{id}/`
**DELETE** `/api/chatbot/faqs/{id}/`

## Admin Panel

Access the Django admin panel at `/admin/`:
1. Navigate to Chatbot section
2. View and manage Chat FAQs
3. Review Chat Messages and conversation history

## Customization

### Modify System Prompt
Edit the `system_prompt` in `chatbot/views.py` -> `ChatbotAPIView._get_openai_response()` to change bot behavior.

### Change AI Model
Replace `gpt-3.5-turbo` with `gpt-4` in `views.py` for more advanced responses (costs more):
```python
response = openai.ChatCompletion.create(
    model="gpt-4",  # Change here
    ...
)
```

### Customize UI
Edit `frontend/src/components/CustomerSupportChat.tsx` to customize colors, position, size, and styling.

## Troubleshooting

**"OPENAI_API_KEY not set" error**
- Make sure your `.env` file is in the project root
- Verify the environment variable is correctly set
- Restart the Django server after setting the environment variable

**Chat not responding**
- Check browser console for errors
- Ensure backend is running on correct port
- Check that `VITE_API_BASE` matches your backend URL

**CORS errors**
- Verify `ALLOWED_HOSTS` includes your frontend URL in `settings.py`
- Check that `corsheaders` is installed and in `INSTALLED_APPS`

## Database Models

### ChatMessage
- `user`: User who initiated chat (nullable for anonymous)
- `session_id`: Unique session identifier
- `user_message`: User's message text
- `bot_response`: Bot's response text
- `created_at`: Timestamp

### ChatFAQ
- `question`: FAQ question
- `answer`: FAQ answer text
- `category`: Category (orders, billing, technical, restaurant, general)
- `active`: Whether FAQ is active
- `created_at`: Timestamp

## Cost Considerations

OpenAI API charges per token used. Typical chat responses use:
- **System prompt**: ~100-200 tokens (fixed)
- **User message**: ~10-50 tokens
- **Bot response**: ~50-150 tokens

**Estimated costs**: $0.001 - $0.005 per conversation

To reduce costs:
- Use conversation history limit (currently 6 messages)
- Use GPT-3.5-turbo instead of GPT-4
- Implement rate limiting

## Next Steps

1. Train your FAQ database with common customer questions
2. Monitor conversation quality in admin panel
3. Integrate with order system for better context
4. Add sentiment analysis to escalate angry customers
5. Implement admin notifications for unresolved issues

