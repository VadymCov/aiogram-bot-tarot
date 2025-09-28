from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from database.operations import get_or_create_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if hasattr(event, "from_user") and event.from_user: # type: ignore
            user_id = event.from_user.id # type: ignore
            user = await get_or_create_user(user_id)
            data["user"] = user
            data["lang"] = user.language

        return await handler(event, data)
