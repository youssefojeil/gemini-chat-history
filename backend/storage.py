import os
import json
import config
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading

# Create a lock for thread-safe file operations
file_lock = threading.Lock()

def ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(config.DATA_DIR, exist_ok=True)

def get_chats_file_path():
    """Get the full path to the chats JSON file."""
    ensure_data_dir()
    return os.path.join(config.DATA_DIR, config.CHATS_FILE)

def read_chats():
    """Read all chats from the JSON file."""
    file_path = get_chats_file_path()
    
    with file_lock:
        if not os.path.exists(file_path):
            # If file doesn't exist, return an empty list
            return []
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If file is empty or invalid JSON, return an empty list
            return []

def write_chats(chats: List[Dict[str, Any]]):
    """Write all chats to the JSON file."""
    file_path = get_chats_file_path()
    
    with file_lock:
        with open(file_path, 'w') as f:
            json.dump(chats, f, indent=2, default=json_serializer)

def get_chat_by_id(chat_id: str) -> Optional[Dict[str, Any]]:
    """Get a chat by its ID."""
    chats = read_chats()
    for chat in chats:
        if chat['_id'] == chat_id:
            return chat
    return None

def add_chat(chat: Dict[str, Any]) -> str:
    """Add a new chat and return its ID."""
    chats = read_chats()
    
    # Generate a simple ID if not provided
    if '_id' not in chat:
        chat['_id'] = generate_id()
    
    # Normalize roles in messages
    if 'messages' in chat:
        for message in chat['messages']:
            # Ensure consistent role naming between frontend and Gemini API
            if message['role'] == 'assistant':
                message['role'] = 'model'
    
    chats.append(chat)
    write_chats(chats)
    return chat['_id']

def update_chat(chat_id: str, updates: Dict[str, Any]) -> bool:
    """Update a chat by its ID."""
    chats = read_chats()
    
    # Normalize roles in messages
    if 'messages' in updates:
        for message in updates['messages']:
            # Ensure consistent role naming between frontend and Gemini API
            if message['role'] == 'assistant':
                message['role'] = 'model'
    
    for i, chat in enumerate(chats):
        if chat['_id'] == chat_id:
            # Update the chat with the new values
            chats[i].update(updates)
            write_chats(chats)
            return True
    
    return False

def delete_chat(chat_id: str) -> bool:
    """Delete a chat by its ID."""
    chats = read_chats()
    initial_count = len(chats)
    
    chats = [chat for chat in chats if chat['_id'] != chat_id]
    
    if len(chats) < initial_count:
        write_chats(chats)
        return True
    
    return False

def add_message_to_chat(chat_id: str, message: Dict[str, Any]) -> bool:
    """Add a message to a chat."""
    chats = read_chats()
    
    # Normalize role naming
    if message['role'] == 'assistant':
        message['role'] = 'model'
    
    for i, chat in enumerate(chats):
        if chat['_id'] == chat_id:
            if 'messages' not in chat:
                chat['messages'] = []
            
            chat['messages'].append(message)
            chat['updated_at'] = datetime.now().isoformat()
            
            write_chats(chats)
            return True
    
    return False

def get_all_chats_without_messages() -> List[Dict[str, Any]]:
    """Get all chats without their messages."""
    chats = read_chats()
    return [{k: v for k, v in chat.items() if k != 'messages'} for chat in chats]

def generate_id() -> str:
    """Generate a simple unique ID."""
    import uuid
    return str(uuid.uuid4())

def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable") 