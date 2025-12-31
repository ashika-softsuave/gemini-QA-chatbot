# Streamlit UI
import streamlit as st
import os
from chat_service import get_chat_history, save_message, clear_chat
from gemini_client import ask_gemini

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Gemini QA Chatbot", layout="centered")

mode = "DEV MODE" if os.getenv("DEV_MODE") == "true" else "AI MODE"
st.caption(f"🔧 {mode}")

st.title("🤖 Gemini QA Chatbot")

# ------------------ USER ID ------------------
user_id = st.text_input("Enter User ID", value="guest")

# ------------------ RESET CHAT ------------------
def reset_chat(user_id):
    clear_chat(user_id)   # clear DB
    st.rerun()

if st.button("🗑 Reset Chat"):
    reset_chat(user_id)

# ------------------ LOAD CHAT HISTORY ------------------
history = get_chat_history(user_id)

# ------------------ DISPLAY HISTORY ------------------
for msg in history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------ USER INPUT ------------------
user_input = st.chat_input("Ask something...")

if user_input:
    # 1️⃣ Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # 2️⃣ Save user message
    save_message(user_id, "user", user_input)

    # 3️⃣ Update history BEFORE calling Gemini
    updated_history = history + [
        {"role": "user", "content": user_input}
    ]

    # 4️⃣ Ask Gemini
    reply = ask_gemini(user_input, updated_history)

    # 5️⃣ Save assistant reply
    save_message(user_id, "assistant", reply)

    # 6️⃣ Display assistant reply
    with st.chat_message("assistant"):
        st.write(reply)
