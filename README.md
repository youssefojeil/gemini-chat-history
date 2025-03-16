# AI Chat App with Gemini

A full-stack chat application using Google's Gemini AI, with a Flask backend and Next.js frontend.

## Features

- Chat with Google's Gemini AI using the chat API
- Maintains conversation context between messages
- Start new conversations
- View and manage chat history
- Modern UI with Tailwind CSS and shadcn/ui
- Local JSON file storage (no database required)

## Project Structure

The project is divided into two main parts:

- `backend/`: Flask backend that communicates with the Gemini API and handles data storage
- `frontend/`: Next.js frontend with a modern UI

## Prerequisites

- Python 3.8+ for the backend
- Node.js 18+ for the frontend
- Google Gemini API key

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd backend
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables by editing the `.env` file:

   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

   You can get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. The application uses a local JSON file for storage. You can configure the storage location in the `.env` file:

   ```
   DATA_DIR=data
   CHATS_FILE=chats.json
   ```

5. Start the Flask server:
   ```
   python app.py
   ```
   The server will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Create a `.env.local` file with:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   ```

4. Start the development server:
   ```
   npm run dev
   ```
   The application will be available at http://localhost:3000

## How It Works

- The backend uses Gemini's chat API with `start_chat()` and `send_message()` methods
- Chat sessions are maintained in memory for better performance
- All messages and responses are stored in a local JSON file
- The frontend communicates with the backend via RESTful API endpoints

## Technologies Used

- **Backend**:

  - Flask
  - Google Generative AI Python SDK (with chat API)
  - Local JSON file for data storage

- **Frontend**:
  - Next.js 14
  - TypeScript
  - Tailwind CSS
  - shadcn/ui components
  - Axios for API requests

## License

MIT
