# 🎯 AI Customer Support Chatbot - Complete Setup Guide

## ✅ What's Been Created

I've built a complete **AI-powered customer support chatbot** for your kitchen management system. Here's what's included:

### Backend (Django)
- ✅ New `chatbot` app with full API
- ✅ AI integration with OpenAI GPT-3.5-turbo
- ✅ FAQ knowledge base system
- ✅ Chat history tracking
- ✅ Django admin interface
- ✅ Database models for messages and FAQs

### Frontend (React)
- ✅ Beautiful floating chat widget
- ✅ Session persistence
- ✅ Real-time messaging UI
- ✅ Loading states and error handling

### Documentation
- ✅ Detailed setup guide (CHATBOT_SETUP.md)
- ✅ Implementation summary (CHATBOT_IMPLEMENTATION.md)
- ✅ Verification test script

---

## 🚀 Getting Started (5 Steps)

### Step 1: Install Dependencies
```bash
# Backend - Install OpenAI SDK
pip install openai

# Frontend - Install UUID library
cd frontend
npm install uuid
cd ..
```

### Step 2: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and save it safely

### Step 3: Configure Environment
Create a `.env` file in your **project root** (same level as manage.py):
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 4: Setup Database
Run these commands:
```bash
# Create tables
python manage.py makemigrations chatbot
python manage.py migrate

# Seed initial FAQs
python manage.py init_faqs
```

### Step 5: Add Chat Widget to Frontend
Edit `frontend/src/App.tsx` and add these imports and component:

```tsx
import CustomerSupportChat from './components/CustomerSupportChat';

function App() {
  return (
    <div>
      {/* Your existing app content */}
      
      {/* Add chatbot at the end */}
      <CustomerSupportChat />
    </div>
  );
}

export default App;
```

---

## ▶️ Running the System

Open **3 separate terminals**:

### Terminal 1: Django Backend
```bash
python manage.py runserver 8000
```
You should see: `Starting development server at http://127.0.0.1:8000/`

### Terminal 2: React Frontend
```bash
cd frontend
npm run dev
```
You should see: `Local: http://localhost:5173/`

### Terminal 3: Verify Setup (Optional)
```bash
python test_chatbot_setup.py
```

---

## 🧪 Testing the Chatbot

1. **Open your frontend** at http://localhost:5173/
2. **Look for the chat button** - blue circle in bottom-right corner
3. **Click the button** to open the chat
4. **Type a message** like:
   - "How do I track my order?"
   - "What's your refund policy?"
   - "Do you deliver to my area?"
5. **Chat with the AI** - it will respond with smart, context-aware answers

---

## 📁 What Was Added/Modified

### New Files Created
```
/chatbot/                          # New Django app
  ├── models.py                    # ChatMessage, ChatFAQ models
  ├── views.py                     # API endpoints + OpenAI logic
  ├── serializers.py               # Request/response serializers
  ├── urls.py                      # API routes
  ├── admin.py                     # Django admin integration
  ├── apps.py                      # App configuration
  ├── tests.py                     # Tests file
  └── management/
      └── commands/
          └── init_faqs.py         # Command to seed FAQs

/frontend/src/components/
  └── CustomerSupportChat.tsx      # React chat widget component

Documentation Files:
  ├── CHATBOT_SETUP.md             # Detailed setup instructions
  ├── CHATBOT_IMPLEMENTATION.md    # Implementation overview
  └── CHATBOT_QUICK_START.md       # This file!

/test_chatbot_setup.py             # Verification script
```

### Modified Files
```
kitchen_system/settings.py         # Added 'chatbot' to INSTALLED_APPS
kitchen_system/urls.py             # Added chatbot URL routing
```

---

## 🌐 API Endpoints

Once running, you can test these endpoints:

### Main Chat Endpoint
```
POST /api/chatbot/
Content-Type: application/json

{
  "message": "How do I track my order?",
  "session_id": "optional-uuid"
}

Response:
{
  "message": "You can track your order in...",
  "session_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### View FAQs
```
GET /api/chatbot/faqs/
GET /api/chatbot/faqs/by_category/?category=orders
```

### View Chat History
```
GET /api/chatbot/history/?session_id=uuid
```

---

## 🎨 Customization Options

### Change Chat Widget Position
Edit `CustomerSupportChat.tsx`:
```tsx
// Change "bottom-4 right-4" to position differently
<button className="fixed bottom-4 right-4 ...">
```

### Change Colors
Search/replace in `CustomerSupportChat.tsx`:
- `bg-blue-600` → your color
- `hover:bg-blue-700` → your hover color

### Change System Prompt
Edit `chatbot/views.py` around line 80:
```python
system_prompt = f"""You are a helpful customer support assistant..."""
```

### Use GPT-4 (More Powerful)
Edit `chatbot/views.py` line 107:
```python
model="gpt-4",  # Instead of "gpt-3.5-turbo"
```

---

## 📚 FAQ Categories

The system comes with 10 pre-seeded FAQs in these categories:

- **orders**: Tracking, delivery, modifications
- **billing**: Payments, refunds, fees
- **technical**: App issues, bugs
- **restaurant**: Hours, location, policies
- **general**: Other questions

You can add more FAQs in Django admin at `/admin/chatbot/chatfaq/`

---

## 💰 Cost Information

**OpenAI Pricing**: $0.002 per 1,000 tokens (GPT-3.5-turbo)

Typical conversation:
- System prompt: ~200 tokens
- User message: ~20 tokens
- Bot response: ~100 tokens
- **Total: ~320 tokens = $0.0006 per chat**

Very affordable! A thousand chats would cost ~$0.60.

---

## 🔒 Security Notes

⚠️ **Keep Your API Key Secret:**
- Never commit `.env` to Git
- Add `.env` to `.gitignore`
- Don't share your key
- Regenerate if accidentally exposed

Add to `.gitignore`:
```
.env
.env.local
```

---

## ⚠️ Troubleshooting

### "OPENAI_API_KEY not set"
- Check `.env` file exists in project root
- Verify key starts with `sk-`
- Restart Django after changing `.env`

### Chat widget doesn't appear
- Check browser console (F12)
- Verify `CustomerSupportChat` component imported in App.tsx
- Ensure frontend is running on correct port

### API errors in console
- Check backend is running (`python manage.py runserver 8000`)
- Verify `VITE_API_BASE` matches backend URL
- Check CORS is enabled

### Database errors
- Run: `python manage.py migrate chatbot`
- Check database permissions

### No FAQs in dropdown
- Run: `python manage.py init_faqs`
- Check FAQs were created in admin

---

## 📊 Next Steps

1. **Test thoroughly** - Try various customer questions
2. **Monitor quality** - Check admin panel for response quality
3. **Add more FAQs** - Build comprehensive knowledge base
4. **Train on data** - Use actual customer questions
5. **Monitor costs** - Track OpenAI usage
6. **Add integrations** - Connect to order system for context
7. **Set rate limits** - Prevent abuse
8. **Gather feedback** - Improve responses based on usage

---

## 📞 Admin Panel

Access at http://localhost:8000/admin/

Manage:
- **Chat FAQs**: Add, edit, delete knowledge base
- **Chat Messages**: View conversation history

---

## 🎓 Learning Resources

- OpenAI Docs: https://platform.openai.com/docs
- Django REST Framework: https://www.django-rest-framework.org/
- React Hooks: https://react.dev/reference/react

---

**You're all set! 🚀**

Start the servers and click the chat button to begin!

Questions? Check CHATBOT_SETUP.md for more details.
