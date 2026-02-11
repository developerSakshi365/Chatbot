from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_bot_response
from datetime import datetime

from database import SessionLocal, User
from auth import (
    hash_password,
    verify_password,
    verify_google_token
)

conversation_memory = {}

app = FastAPI()

# ---------- CORS (VERY IMPORTANT FOR REACT) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- REQUEST MODELS ----------

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class GoogleLoginRequest(BaseModel):
    token: str


class ChatRequest(BaseModel):
    message: str


def log_chat(user_message, bot_reply):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(
            f"Time: {datetime.now()}\n"
            f"User: {user_message}\n"
            f"Bot: {bot_reply}\n"
            f"{'-' * 40}\n"
        )


# ---------- ROUTES ----------

@app.get("/")
def home():
    return {"status": "Backend is running"}


# ---------- NORMAL SIGNUP ----------
@app.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "Signup successful",
            "name": user.name,
            "email": user.email
        }
    finally:
        db.close()


# ---------- NORMAL LOGIN ----------
@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "Login successful",
            "name": user.name,
            "email": user.email
        }
    finally:
        db.close()


# ---------- GOOGLE LOGIN ----------
@app.post("/google-login")
def google_login(data: GoogleLoginRequest):
    google_user = verify_google_token(data.token)

    if not google_user:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = google_user["email"]
    name = google_user.get("name", email.split("@")[0])

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        # If user does not exist → create
        if not user:
            user = User(
                name=name,
                email=email,
                password="GOOGLE_AUTH"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return {
            "message": "Google login successful",
            "name": user.name,
            "email": user.email
        }
    finally:
        db.close()


@app.post("/chat")
def chat(data: ChatRequest):
    try:
        user_id = "default_user"  # you can later replace with logged-in user

        if user_id not in conversation_memory:
            conversation_memory[user_id] = []

        # Save user message
        conversation_memory[user_id].append({
            "role": "user",
            "content": data.message
        })

        # Keep last 10 messages only
        conversation_memory[user_id] = conversation_memory[user_id][-10:]

        # Get bot reply using the imported function
        bot_reply = get_bot_response(
            data.message,
            conversation_memory[user_id]
        )

        # Save bot reply
        conversation_memory[user_id].append({
            "role": "bot",
            "content": bot_reply
        })

        # Log interaction
        log_chat(data.message, bot_reply)

        return {"reply": bot_reply}

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")