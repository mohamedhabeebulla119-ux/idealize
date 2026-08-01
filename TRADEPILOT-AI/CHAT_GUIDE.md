# TradePilot AI Chat Interface - Quick Guide

## Overview

TradePilot AI is a ChatGPT-like conversational interface that connects to multiple specialized agents to help with import/export compliance, risk analysis, workflow planning, and more.

## How It Works

### Chat Flow
1. **User Input** → You ask a question or request
2. **Intent Detection** → The system identifies what you're asking about
3. **Agent Routing** → Automatically routes to the appropriate agent
4. **Knowledge Retrieval** → RAG system finds relevant information
5. **AI Response** → Agent generates comprehensive answer
6. **Display** → Response shown in conversation format

### Available Agents

| Agent | What It Does | Example Queries |
|-------|-------------|-----------------|
| **Workflow Agent** | Plans import/export workflows | "What are the export steps for tea to UK?", "How do I import motorcycles?" |
| **Compliance Agent** | Checks regulations & requirements | "What are cinnamon export requirements?", "Compliance checklist for electronics" |
| **Risk Agent** | Analyzes potential risks | "What are the risks of importing motorcycles?", "Identify risks for tea export" |
| **Checklist Agent** | Creates readiness checklists | "Give me a checklist for exporting cinnamon", "Readiness assessment for imports" |
| **Tariff Agent** | Searches tariff codes & rates | "What's the HS code for electronics?", "Tariff information for tea" |
| **Document Agent** | Verifies documents | Upload & verify export/import documents |
| **Cost Agent** | Estimates costs | "Estimate costs for motorcycle import", "Calculate export costs" |

## Example Conversations

### Example 1: Export Planning
```
User: "I want to export tea to the UK, what do I need to do?"

Bot: [Shows workflow steps]
    1. Verify tea meets UK standards
    2. Obtain export license
    3. Arrange documentation
    4. ...

User: "What are the compliance requirements?"

Bot: [Shows compliance details]
    - Food safety certifications
    - Packaging requirements
    - Labeling standards
    - ...

User: "What about risks?"

Bot: [Shows risk analysis]
    - Supply chain disruptions
    - Quality issues
    - Regulatory changes
    - ...
```

### Example 2: Import Analysis
```
User: "I'm thinking about importing motorcycles from Japan"

Bot: [Shows workflow and requirements]

User: "How much will it cost?"

Bot: [Shows cost breakdown]
    - Tariff fees
    - Inspection costs
    - Registration fees
    - ...

User: "What documents do I need?"

Bot: [Shows document checklist]
```

## Features

### 💬 Conversation Management
- **New Chat** - Start a fresh conversation
- **History** - View all past conversations in sidebar
- **Context** - Each conversation maintains context for follow-up questions
- **Delete** - Remove conversations you don't need

### 🎯 Intent Recognition
- Automatically understands what you're asking
- Shown as "Intent: [type]" in responses
- Helps route to the right agent

### 📋 Response Formatting
- **Workflows** - Numbered steps
- **Compliance** - Organized requirements
- **Risks** - Categorized risk items
- **Checklists** - Checkboxes for tracking

### ⚡ Quick Examples
- Click any example prompt at startup
- Covers common use cases
- Get started instantly

### 🌐 Mobile Responsive
- Works on desktop, tablet, phone
- Touch-friendly interface
- Sidebar collapses on mobile

## Tips & Tricks

### 1. Be Specific
**Better:** "What are the export requirements for cinnamon to India?"
**Not as good:** "Requirements?"

### 2. Provide Context
**Better:** "I'm exporting electronics from Sri Lanka to USA"
**Not as good:** "Export electronics"

### 3. Multi-turn Conversations
You can ask follow-up questions and the bot remembers context:
```
User: "What are the export steps for tea?"
Bot: [Shows workflow]
User: "What about compliance?" ← Uses context from previous message
Bot: [Shows compliance for tea export]
```

### 4. Try Different Angles
If response doesn't meet your need, rephrase:
```
"Requirements for cinnamon export" vs "How do I export cinnamon"
"Risks of motorcycle import" vs "What problems might I face importing motorcycles"
```

### 5. Multi-step Planning
Build your plan step by step:
1. Ask about workflow
2. Ask about compliance
3. Ask about risks
4. Ask about costs
5. Get final checklist

## Common Questions

### Q: Why is the response incomplete?
**A:** Try asking a more specific question or break it into multiple questions.

### Q: How do I export this conversation?
**A:** Copy the text from the chat or take a screenshot. Future versions will have export.

### Q: Can I edit a previous message?
**A:** Start a new conversation. Each conversation is independent.

### Q: Is my conversation data saved?
**A:** Conversations are saved in browser storage. They're not sent to external servers.

### Q: What if the bot gives wrong information?
**A:** The bot uses knowledge base and AI models which can sometimes be inaccurate. Always verify critical information with official sources.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl + L` (Cmd + L on Mac) | Clear chat (coming soon) |

## API Reference for Developers

See `SETUP_GUIDE.md` for backend API details and integration instructions.

## Troubleshooting

### Issue: Bot says "Error" or no response
- Check internet connection
- Refresh the page
- Check if backend is running (`http://localhost:8000/docs`)
- Try a simpler question

### Issue: Responses are irrelevant
- Provide more context in your question
- Be specific about trade type (import/export)
- Mention specific products or countries

### Issue: Chat is slow
- Backend might be processing
- Check if vector database is initialized
- Larger queries take longer

## Next Steps

1. **Try it out!** Start with an example prompt
2. **Ask questions** about your specific trade scenario
3. **Build your plan** using multi-turn conversations
4. **Export results** when needed
5. **Share feedback** about what works

## Support & Feedback

- Check API docs: `http://localhost:8000/docs`
- Review logs in terminal windows
- Share suggestions for improvement

---

**Happy Trading! 🚀**

For technical setup, see `SETUP_GUIDE.md`
For project details, see `PROJECT_OVERVIEW.md`
