from database.operations import get_or_create_user
from datetime import datetime, date
import time
from typing import Any
import asyncio
import aiofiles
import random
import json


class CardService:
    _lang_cashe: dict[str, dict[str, Any]] = {}
    _cashe_timestamps: dict[str, float] = {}
    CACHE_TTL = 2000

    @classmethod
    async def _load_language(cls, lang: str):
        async with aiofiles.open(f"data/cards/{lang}.json", "r")as f:
            content = await f.read()
            cards_descriptions = await asyncio.to_thread(json.loads, content)

        cls._lang_cashe[lang] = cards_descriptions["cards"]
        cls._cashe_timestamps[lang] = time.time()