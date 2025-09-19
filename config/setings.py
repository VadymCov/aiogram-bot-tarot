import os
from dataclasses import dataclass

@dataclass
class Settings:
    """Application settings class"""

    BOT_TOKEN: str = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

    # API for photo
    PIXELS_API_KEY: str | None = os.getenv('PIXELS_API_KEY')
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'tarot_bot.db')
    # Scheduler
    HOROSCOPE_SEND_TIME: str = os.getenv('HOROSCOPE_SEND_TIME', '8:00')
    # Webhook for production
    WEBHOOK_URL: str | None = os.getenv('WEBHOOK_URL')
    WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH', '/webhook')
    WEBAPP_HOST: str = os.getenv('WEBAPP_HOST', 'localhost')
    WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT', '8080'))

    # Admins 
    ADMIN_IDS: list[int] = [
        int(admin_id) for admin_id in os.getenv('ADMIN_IDS', '').split(',') if admin_id.strip()
    ]

    def __post_init__(self):
        if self.BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            raise ValueError("BOT_TOKEN unspecified")
        
    @property
    def is_development(self) -> bool:
        return os.getenv("ENVIRONMENT", "development") == "development"
    
    @property
    def is_production(self) -> bool:
        return os.getenv("ENVIRONMENT") == "production"