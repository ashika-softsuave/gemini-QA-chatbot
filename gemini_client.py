# Gemini API Logic
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

DEV_MODE = os.getenv("DEV_MODE") == "true"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(user_input, history):
    if DEV_MODE:
        return f"[DEV MODE] Reply for: {user_input}"

    contents = []

    for msg in history:
        role = "user" if msg["role"] == "user" else "model"

        contents.append({
        "role": role,
        "parts": [{"text": msg["content"]}]
    })


    contents.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=contents
    )

    return response.text
