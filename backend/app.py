from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
from datetime import datetime
import config
import storage

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=config.GEMINI_API_KEY)

# Dictionary to store active chat sessions
active_chats = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    chat_id = data.get('chatId')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Generate response from Gemini
    try:
        timestamp = datetime.now().isoformat()
        
        if chat_id:
            # Add to existing chat
            chat_data = storage.get_chat_by_id(chat_id)
            if not chat_data:
                return jsonify({'error': 'Chat not found'}), 404
            
            # Add user message to storage
            storage.add_message_to_chat(chat_id, {
                'role': 'user',
                'content': message,
                'timestamp': timestamp
            })
            
            # Check if we have an active chat session for this chat_id
            if chat_id in active_chats:
                chat_session = active_chats[chat_id]
            else:
                # Create a new chat session with history from storage
                model = genai.GenerativeModel(config.GEMINI_MODEL)
                
                # Convert stored messages to the format expected by Gemini
                history = []
                for msg in chat_data.get('messages', []):
                    history.append({
                        "role": msg['role'],
                        "parts": [{"text": msg['content']}]
                    })
                
                # Initialize chat with history
                chat_session = model.start_chat(history=history)
                active_chats[chat_id] = chat_session
            
            # Send message to Gemini
            response = chat_session.send_message(message)
            ai_response = response.text
            
            # Add assistant message to storage
            storage.add_message_to_chat(chat_id, {
                'role': 'model',  # Gemini uses 'model' as role
                'content': ai_response,
                'timestamp': timestamp
            })
        else:
            # Create new chat
            model = genai.GenerativeModel(config.GEMINI_MODEL)
            chat_session = model.start_chat()
            
            # Send first message
            response = chat_session.send_message(message)
            ai_response = response.text
            
            # Create a new chat in storage
            chat_title = message[:30] + "..." if len(message) > 30 else message
            chat_id = storage.add_chat({
                'title': chat_title,
                'created_at': timestamp,
                'updated_at': timestamp,
                'messages': [
                    {
                        'role': 'user',
                        'content': message,
                        'timestamp': timestamp
                    },
                    {
                        'role': 'model',  # Gemini uses 'model' as role
                        'content': ai_response,
                        'timestamp': timestamp
                    }
                ]
            })
            
            # Store the chat session for future use
            active_chats[chat_id] = chat_session
        
        return jsonify({
            'response': ai_response,
            'chatId': chat_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chats', methods=['GET'])
def get_chats():
    try:
        chats = storage.get_all_chats_without_messages()
        # Sort by updated_at in descending order
        chats.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return jsonify(chats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        chat = storage.get_chat_by_id(chat_id)
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        
        # Convert 'model' role to 'assistant' for frontend compatibility
        for message in chat.get('messages', []):
            if message['role'] == 'model':
                message['role'] = 'assistant'
                
        return jsonify(chat)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        success = storage.delete_chat(chat_id)
        if not success:
            return jsonify({'error': 'Chat not found'}), 404
        
        # Remove from active chats if present
        if chat_id in active_chats:
            del active_chats[chat_id]
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure data directory exists
    storage.ensure_data_dir()
    app.run(debug=config.DEBUG)
