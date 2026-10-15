# Career Chatbot: Ask Me Anything About My Work
 
An AI-powered chatbot that lives on my website and answers questions about my background, skills, and experience, so recruiters and collaborators can get answers instantly, any time of day.
 
**Live demo:** [https://your-app.onrender.com](https://twin-chat-agent.onrender.com/)
 
> The demo runs on a free hosting tier, so the first visit after a period of inactivity can take up to a minute to wake up.
 
---
 
## What it does
 
- **Answers questions about me.** The chatbot is grounded in my LinkedIn PDF and a written summary, so it responds from real information instead of guessing.
- **Collects contact details.** If a visitor wants to stay in touch, the bot asks for their email (and name, if they offer it) and records it using a tool call.
- **Flags questions it can't answer.** Any question outside its knowledge is logged, so I can see the gaps and improve the bot's context over time.
- **Notifies my phone.** Contact details and unanswered questions are sent to me instantly through [Pushover](https://pushover.net/).
## How it works
 
```
Visitor ──► Gradio chat UI ──► LLM (with system prompt + PDF + summary)
                                   │
                                   ├── tool: record_user_details ──► Pushover ──► my phone
                                   └── tool: record_unknown_question ──► Pushover ──► my phone
```
 
1. On startup, the app loads the text from my LinkedIn PDF and `summary.txt`.
2. Both are injected into the system prompt, which tells the model to act as me and stay faithful to that information.
3. The model has two tools available through function calling:
   - `record_user_details(email, name, notes)` is called when a visitor wants to get in touch.
   - `record_unknown_question(question)` is called when the model can't answer from the provided context.
4. Each tool call sends a push notification through the Pushover API.
## Tech stack
 
- **Python**
- **Gradio** for the chat interface
- **LLM API** with tool/function calling (`<your provider and model>`)
- **pypdf** for reading the PDF
- **Pushover** for mobile notifications
- **Render** for hosting
