# Tarot Bot

Telegram bot for daily tarot readings, family advice, and personal spiritual guidance.

## Features

-  Daily card readings (Vadaram & Obusha decks)
-  Ancestral wisdom & family advice
-  Birth date tracking for personalized readings
-  Multi-language support (UA/EN/RU)
-  Birthday greetings
-  User settings management

## Screenshots

<div align="center">
  <img src="screenshots/main_menu.png" width="200" alt="Main Menu"/>
  <img src="screenshots/card_reading.png" width="200" alt="Card Reading"/>
  <img src="screenshots/settings.png" width="200" alt="Settings"/>
  <img src="screenshots/calendar.png" width="200" alt="Birth Date"/>
</div>

## Tech Stack

- **Python 3.11+**
- **aiogram 3.x** - Telegram Bot framework
- **SQLAlchemy** - async ORM
- **PostgreSQL** - database
- **aiogram-calendar** - date picker

## Setup

1. **Clone & install**
```bash
git clone <repo-url>
cd <project-name>
pip install -r requirements.txt
```

2. **Configure environment**
```bash
# .env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
```

3. **Run**
```bash
python main.py
```

## Project Structure
```
├── bot/
│   ├── handlers/          # Command & callback handlers
│   ├── keyboards/         # Inline keyboards
│   └── middlewares/       # User data middleware
├── database/
│   ├── models.py          # SQLAlchemy models
│   └── operations.py      # DB queries
├── services/
│   ├── card_service.py    # Card/media management
│   └── user_service.py    # User operations
├── data/
│   ├── desc_cards/        # Card descriptions (lang)
│   ├── media_ids/         # Telegram file IDs
│   └── text_*.json        # UI texts
└── main.py
```

## Key Files

- `main.py` - Bot initialization & startup
- `database/models.py` - User model with readings tracking
- `services/card_service.py` - Caching layer for cards/media
- `bot/handlers/` - All bot logic (cards, calendar, settings)

## Database Schema
```sql
users (
  id SERIAL PRIMARY KEY,
  telegram_id BIGINT UNIQUE,
  language VARCHAR(3) DEFAULT 'ua',
  gender VARCHAR(10),
  birth_date DATE,
  last_card_date DATE,
  last_vadaram_date DATE,
  last_obusha_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
)
```

## License

MIT

