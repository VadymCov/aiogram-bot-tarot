from database.operations import get_or_create_user
from datetime import datetime, date
import time
from typing import Any
import asyncio
import aiofiles
import random
import json

import logging

logger = logging.getLogger(__name__)


class CardService:
    _lang_desc_cache: dict[str, dict[str, Any]] = {}
    _cache_timestamps: dict[str, float] = {}
    _media_cache: dict[str, dict[str, str]] = {}
    _lang_media_cache: dict[str, dict[str, str]] = {}
    CACHE_TTL = 3600

    @classmethod
    async def _load_media_ids(cls, deck_name: str):
        file_path = f"data/media_ids/{deck_name}_ids.json"
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                media_ids = await asyncio.to_thread(json.loads, content)
            cls._media_cache[deck_name] = media_ids
        except FileNotFoundError:
            logger.info(f"❌ File ID for deck no found")
            raise

    @classmethod
    async def get_media_id(cls, deck_name: str, card_number: str):
        if deck_name not in cls._media_cache:
            await cls._load_media_ids(deck_name)
        return cls._media_cache[deck_name][card_number]

    @classmethod
    async def _load_language_desc(cls, lang: str):
        async with aiofiles.open(f"data/cards/{lang}.json", "r", encoding="utf-8") as f:
            content = await f.read()
            cards_descriptions = await asyncio.to_thread(json.loads, content)

        cls._lang_desc_cache[lang] = cards_descriptions["cards"]
        cls._cache_timestamps[lang] = time.time()

    @classmethod
    async def get_card_descriptions(cls, card_number: str, lang: str):
        if lang not in cls._lang_desc_cache:
            await cls._load_language_desc(lang)

        if time.time() - cls._cache_timestamps[lang] > cls.CACHE_TTL:
            await cls._load_language_desc(lang)

        return cls._lang_desc_cache[lang][card_number]

    @classmethod
    async def _load_language_media_ids(cls, deck_name, lang: str):
        file_path = f"data/media_ids/lang_media_ids/{deck_name}/{lang}.json"
        try:
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
                media_ids = await asyncio.to_thread(json.loads, content)
            cls._lang_media_cache[deck_name][lang] = media_ids
        except FileNotFoundError:
            logger.exception(f"❌ File ID for deck {deck_name} and lang {lang} not found")
            raise