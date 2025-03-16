# AI Chat App Backend

This is the Flask backend for the AI Chat application using Google's Gemini API.

## Features

- Uses Gemini's chat API with `start_chat` and `send_message` methods
- Maintains chat history and context between messages
- Stores conversations in a local JSON file
- RESTful API endpoints for chat management

## Setup

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables by editing the `.env` file:

   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

   You can get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. The application uses a local JSON file for storage. You can configure the storage location in the `.env` file:

   ```
   DATA_DIR=data
   CHATS_FILE=chats.json
   ```

## Running the Application

Start the Flask server:

```
python app.py
```

The server will run on http://localhost:5000 by default.

## API Endpoints

- `POST /api/chat` - Send a message to Gemini and get a response
- `GET /api/chats` - Get a list of all chat sessions
- `GET /api/chats/<chat_id>` - Get details of a specific chat session
- `DELETE /api/chats/<chat_id>` - Delete a chat session

## Data Storage

Chat data is stored in a JSON file located at `DATA_DIR/CHATS_FILE` (default: `data/chats.json`). The file is created automatically when the first chat is saved.

## How It Works

1. When a new chat is started, the backend creates a new Gemini chat session using `start_chat()`
2. For existing chats, the backend loads the chat history and initializes a chat session with that history
3. Messages are sent to Gemini using `send_message()` which maintains context between messages
4. Active chat sessions are kept in memory for better performance
5. All messages and responses are stored in the JSON file for persistence
