#MongoDB Setup
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["gemini_chat"]
chat_collection = db["messages"]
