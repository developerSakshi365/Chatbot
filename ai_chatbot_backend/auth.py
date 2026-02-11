from passlib.context import CryptContext
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Google Client ID (from environment variable)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# ---------- PASSWORD FUNCTIONS ----------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------- GOOGLE TOKEN VERIFY ----------

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", "")
        }

    except Exception as e:
        print("Google token error:", e)
        return None
