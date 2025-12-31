#FASTAPI API
from fastapi import FastAPI, HTTPException,Request
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from rate_limiter import limiter

from schemas import ChatRequest, ChatResponse
from chat_service import save_message, get_last_messages, clear_chat
from gemini_client import ask_gemini

app = FastAPI(title="Gemini QA API")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
def chat(request: Request,req: ChatRequest):
    try:
        history = get_last_messages(req.user_id)

        reply = ask_gemini(req.message, history)

        save_message(req.user_id, "user", req.message)
        save_message(req.user_id, "assistant", reply)

        return {"reply": reply}

    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/{user_id}")
def reset_chat(user_id: str):
    clear_chat(user_id)
    return {"message": "Chat cleared"}
