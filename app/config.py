from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore', env_file=".env")
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "Price Monitor"
    APP_VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: str = "*"
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str
    CHECK_INTERVAL_HOURS: int = 6

settings = Settings()