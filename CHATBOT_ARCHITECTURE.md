# 🤖 Customer Support Chatbot - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────┐                       │
│  │   React Frontend (React App)         │                       │
│  │  ┌────────────────────────────────┐  │                       │
│  │  │  CustomerSupportChat Component │  │                       │
│  │  │  ┌──────────────────────────┐  │  │                       │
│  │  │  │  Floating Chat Widget    │  │  │                       │
│  │  │  │  - Message bubbles       │  │  │                       │
│  │  │  │  - Input field           │  │  │                       │
│  │  │  │  - Loading states        │  │  │                       │
│  │  │  └──────────────────────────┘  │  │                       │
│  │  │                                  │  │                       │
│  │  │  sessionStorage                  │  │                       │
│  │  │  [chatSessionId] ────────────┐  │  │                       │
│  │  └────────────────────────────────┘  │                       │
│  └──────────────────────────────────────┘                       │
│              HTTP Fetch API                                      │
│                    ▼                                              │
│                [POST] /api/chatbot/                              │
│            {message, session_id}                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              DJANGO BACKEND (Port 8000)                          │
├─────────────────────────────────────────────────────────────────┤

> See also: [Swimlane diagram](./CHATBOT_SWIMLANE_DIAGRAM.md)
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         ChatbotAPIView (REST Endpoint)                   │   │
│  │  POST /api/chatbot/                                      │   │
│  │  1. Validate request                                     │   │
│  │  2. Generate/get session_id                              │   │
│  │  3. Call _get_bot_response()                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                         │
│                    ┌────┴─────────────────────────┐              │
│                    ▼                              ▼              │
│         ┌─────────────────────┐      ┌──────────────────────┐   │
│         │  _get_openai_       │      │ _get_fallback_       │   │
│         │  response()         │      │ response()           │   │
│         │                     │      │                      │   │
│         │  1. Get chat        │      │ Uses FAQ matching    │   │
│         │     history         │      │ when OpenAI fails    │   │
│         │  2. Get relevant    │      │                      │   │
│         │     FAQs            │      │ Returns generic      │   │
│         │  3. Build system    │      │ helpful response     │   │
│         │     prompt          │      │                      │   │
│         │  4. Call OpenAI     │      └──────────────────────┘   │
│         │     API             │                                   │
│         │  5. Parse response  │                                   │
│         └─────────────────────┘                                   │
│                    │                                              │
│                    ▼ (if configured)                             │
│         ┌──────────────────────┐                                │
│         │  OpenAI API          │                                │
│         │  (External Service)  │                                │
│         │                      │                                │
│         │  GPT-3.5-turbo       │                                │
│         │  or GPT-4            │                                │
│         └──────────────────────┘                                │
│                    ▼                                              │
│         ┌──────────────────────┐                                │
│         │  AI Response         │                                │
│         │  (Context-aware)     │                                │
│         └──────────────────────┘                                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   Database (SQLite)                                      │   │
│  │  ┌──────────────────┐      ┌──────────────────────────┐  │   │
│  │  │  ChatMessage     │      │  ChatFAQ                 │  │   │
│  │  │  - id            │      │  - id                    │  │   │
│  │  │  - user_id       │      │  - question              │  │   │
│  │  │  - session_id    │      │  - answer                │  │   │
│  │  │  - user_message  │      │  - category              │  │   │
│  │  │  - bot_response  │      │  - active                │  │   │
│  │  │  - created_at    │      │  - created_at            │  │   │
│  │  └──────────────────┘      └──────────────────────────┘  │   │
│  │  ▲                         ▲                              │   │
│  │  │ Store conversation      │ Query relevant FAQs        │   │
│  │  └─────────────────────────┴──────────────────────────────┤   │
│  │                                                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   Django Admin Interface                                 │   │
│  │   /admin/chatbot/                                        │   │
│  │  - View & manage FAQs                                    │   │
│  │  - View chat history                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Sequence

```
User Message Flow
═════════════════

1. User clicks chat widget
2. User types message
3. User presses Send
   └─> generateError validation
   └─> Send to backend: POST /api/chatbot/ + {message, session_id}

4. Django receives request
   └─> ChatbotAPIView.post()
   └─> Parse message, session_id
   └─> Call _get_bot_response(message, session_id)

5. Get Bot Response
   ├─> Get chat history from DB (last 6 messages)
   ├─> Search FAQs for relevant matches
   ├─> Try OpenAI API:
   │   ├─> Build system prompt with FAQ context
   │   ├─> Include conversation history
   │   ├─> Add current user message
   │   ├─> Send to OpenAI GPT-3.5-turbo
   │   └─> Return smart response
   ├─> If OpenAI fails:
   │   └─> Use _get_fallback_response()
   │   └─> Return FAQ-based response

6. Save to Database
   └─> Create ChatMessage record:
       ├─> user = current_user (or None)
       ├─> session_id
       ├─> user_message
       ├─> bot_response
       └─> created_at = now()

7. Send Response to Frontend
   └─> Return JSON: {message, session_id, timestamp}

8. Update UI
   └─> Add message pair to chat
   └─> Scroll to bottom
   └─> Clear input field
   └─> Show message in UI
```

## Component Interaction

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │
         │ 1. User types message
         │ 2. Click Send
         │ 3. POST /api/chatbot/
         ▼
┌─────────────────────────────────────┐
│   Django Views                       │
│   ChatbotAPIView                    │
│   - Validate input                  │
│   - Get/create session_id           │
│   - Call _get_bot_response()        │
└────────┬────────────────────────────┘
         │
         ├─────────────────────┬──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
    ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐
    │ Chat History   │  │ FAQ Search  │  │ OpenAI API Call  │
    │                │  │             │  │                  │
    │ SELECT FROM    │  │ KEYWORDS:   │  │ GPT-3.5-turbo    │
    │ ChatMessage    │  │ "order"     │  │                  │
    │ WHERE          │  │ "track"     │  │ Returns:         │
    │ session_id=X   │  │ "delivery"  │  │ Contextual      │
    │                │  │ ...         │  │ response         │
    │ LIMIT 6        │  │             │  │                  │
    └────────────────┘  └─────────────┘  └──────────────────┘
         │                     │                      │
         └─────────┬───────────┴──────────────────────┘
                   │
         ┌─────────▼──────────┐
         │ Combine context:   │
         │ 1. System prompt   │
         │ 2. Chat history    │
         │ 3. Relevant FAQs   │
         │ 4. Current message │
         └─────────┬──────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ Generate response   │
         │ via OpenAI or FAQ   │
         └─────────┬───────────┘
                   │
         ┌─────────▼──────────────┐
         │ Save to database:      │
         │ ChatMessage.objects    │
         │ .create(...)           │
         └─────────┬──────────────┘
                   │
         ┌─────────▼────────────┐
         │ Return to frontend   │
         │ JSON response        │
         │ {message, timestamp} │
         └─────────┬────────────┘
                   │
                   ▼
         ┌──────────────────────┐
         │ Update React state   │
         │ Add messages to list │
         │ Re-render chat UI    │
         └──────────────────────┘
```

## Environment Setup

```
┌──────────────────────────────┐
│  Project Root                │
│  ├─ .env                     │  ← OPENAI_API_KEY=sk-...
│  ├─ manage.py                │
│  ├─ kitchen_system/          │
│  │  ├─ settings.py           │  ← Added 'chatbot' app
│  │  └─ urls.py               │  ← Added chatbot routes
│  │                            │
│  ├─ chatbot/                 │  ← New app
│  │  ├─ models.py             │
│  │  ├─ views.py              │
│  │  ├─ urls.py               │
│  │  ├─ serializers.py        │
│  │  ├─ admin.py              │
│  │  └─ management/commands/  │
│  │     └─ init_faqs.py       │
│  │                            │
│  ├─ frontend/                │
│  │  ├─ src/                  │
│  │  │  ├─ components/        │
│  │  │  │  └─ CustomerSupportChat.tsx  ← New
│  │  │  └─ App.tsx            │  ← Import chat
│  │  └─ package.json          │  ← Add uuid
│  │                            │
│  └─ db.sqlite3               │
│
└──────────────────────────────┘
```

## Database Schema

```
ChatMessage Table
─────────────────
id (PK)          INTEGER PRIMARY KEY
user_id (FK)     INTEGER (nullable) → auth_user.id
session_id       VARCHAR(255) INDEX
user_message     TEXT
bot_response     TEXT
created_at       DATETIME INDEX

Index: (session_id, -created_at)


ChatFAQ Table
─────────────
id (PK)          INTEGER PRIMARY KEY
question         VARCHAR(500)
answer           TEXT
category         VARCHAR(50) CHOICES
                 - 'orders'
                 - 'billing'
                 - 'technical'
                 - 'restaurant'
                 - 'general'
active           BOOLEAN
created_at       DATETIME

Index: (category, question)
```

---

**This architecture enables:**
- ✅ Fast response times (cached FAQs)
- ✅ Graceful degradation (fallback if API fails)
- ✅ Session continuity (browser storage)
- ✅ Analytics (all conversations saved)
- ✅ Admin control (manage FAQs easily)
- ✅ Scalability (stateless API)
