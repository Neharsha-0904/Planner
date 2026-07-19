from pathlib import Path
from pydantic_settings import BaseSettings

# Look for .env in backend/ first, then project root
_env_file = Path(__file__).resolve().parent.parent / ".env"
if not _env_file.exists():
    _env_file = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://planner:planner@localhost:5432/planner"
    SECRET_KEY: str = "change-me-to-a-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    MORNING_BRIEF_HOUR: int = 7
    USER_TIMEZONE: str = "Asia/Kolkata"

    # Email (Gmail SMTP — use App Password, not your regular password)
    EMAIL_BACKEND: str = "smtp"  # "smtp" or "console"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # your Gmail address
    SMTP_PASSWORD: str = ""  # Gmail App Password (16-char)
    SMTP_FROM_NAME: str = "Planner"

    ANTHROPIC_API_KEY: str = ""

    FIREBASE_CREDENTIALS_PATH: str = ""

    model_config = {"env_file": str(_env_file), "extra": "ignore"}


settings = Settings()
