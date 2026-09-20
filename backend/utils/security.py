from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password: str): return pwd_context.hash(password)
def verify_password(password: str, hashed: str): return pwd_context.verify(password, hashed)
def create_token(user_id: int, role: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({'sub': str(user_id), 'role': role, 'exp': exp}, settings.secret_key, algorithm='HS256')
def decode_token(token: str): return jwt.decode(token, settings.secret_key, algorithms=['HS256'])
