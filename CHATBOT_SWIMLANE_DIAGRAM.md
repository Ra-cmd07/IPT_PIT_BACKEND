# Chatbot Swimlane Diagram

This swimlane diagram shows the end-to-end flow for the customer support chatbot, including the user frontend, Django backend, database, and external OpenAI API.

```text
User Browser        Frontend (React)        Django Backend        Database           OpenAI API
-----------------------------------------------------------------------------------------------
User clicks chat -->|                       |                     |                   |
                    |                       |                     |                   |
User types message ->|                       |                     |                   |
                    |                       |                     |                   |
User sends message ->|  POST /api/chatbot/   |                     |                   |
                    |---------------------->|                     |                   |
                    |                       |  ChatbotAPIView.post |                   |
                    |                       |  - validate request  |                   |
                    |                       |  - get/create session|                   |
                    |                       |  - call _get_bot_response() |
                    |                       |                     |                   |
                    |                       |  query ChatMessage   |<------------------|
                    |                       |  WHERE session_id   |                   |
                    |                       |  ORDER BY created_at|                   |
                    |                       |  LIMIT 6             |                   |
                    |                       |                     |                   |
                    |                       |  query ChatFAQ for   |<------------------|
                    |                       |  relevant matches    |                   |
                    |                       |                     |                   |
                    |                       |-- Build prompt ---> |                   |
                    |                       |                     |                   |
                    |                       |  call OpenAI API     |------------------>
                    |                       |  with prompt         |                   |
                    |                       |                     |                   |
                    |                       |  receive AI response |<------------------|
                    |                       |                     |                   |
                    |                       |  if OpenAI fails     |                   |
                    |                       |  use FAQ fallback     |                   |
                    |                       |                     |                   |
                    |                       |  save ChatMessage    |------------------>
                    |                       |  to database          |                   |
                    |                       |                     |                   |
                    |<----------------------|                     |                   |
                    |  return JSON response |                     |                   |
                    |  {message, session_id} |                     |                   |
                    |                       |                     |                   |
UI updates messages  |                       |                     |                   |
-----------------------------------------------------------------------------------------------
```

## Notes

- The frontend stores `session_id` in browser storage and sends it with each chat message.
- The backend attempts an OpenAI response first, with a FAQ fallback for reliability.
- Conversation history and FAQ context are combined into the prompt before calling the AI.
- The database stores every chat message so full session continuity is preserved.
