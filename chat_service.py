
#Chat History Logic
from db import chat_collection

def save_message(user_id, role, content):
    chat_collection.insert_one({
        "user_id": user_id,
        "role": role,
        "content": content
    })

def get_last_messages(user_id, limit=10):
    msgs = list(
        chat_collection.find({"user_id": user_id})
        .sort("_id", 1)
    )
    return msgs[-limit:]

def clear_chat(user_id):
    chat_collection.delete_many({"user_id": user_id})
