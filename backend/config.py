import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_host = os.getenv('DATABASE_HOST', 'localhost')
    database_port = int(os.getenv('DATABASE_PORT', '3306'))
    database_name = os.getenv('DATABASE_NAME', 'nicoedu')
    database_user = os.getenv('DATABASE_USER', 'root')
    database_password = os.getenv('DATABASE_PASSWORD', '')
    secret_key = os.getenv('SECRET_KEY', 'development-only-change-me')
    access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '480'))
    ai_provider = os.getenv('AI_PROVIDER', '').lower()
    ai_api_key = os.getenv('AI_API_KEY', '')
    ai_model = os.getenv('AI_MODEL', '')
    cors_origins = [origin.strip() for origin in os.getenv(
        'CORS_ORIGINS',
        'http://localhost:5500,http://127.0.0.1:5500'
    ).split(',') if origin.strip()]

settings = Settings()
