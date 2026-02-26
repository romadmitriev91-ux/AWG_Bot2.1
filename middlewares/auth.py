from typing import Callable, Dict, Any, Awaitable, List
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class AuthMiddleware(BaseMiddleware):
    """Мидлварь для проверки авторизации администраторов"""
    
    def __init__(self, admin_ids: List[int]):
        self.admin_ids = admin_ids
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Проверка доступа пользователя"""
        
        user_id = event.from_user.id
        is_admin = bool(self.admin_ids and user_id in self.admin_ids)
        data["is_admin"] = is_admin
        data["user_id"] = user_id
        # обычным пользователям не отправляем сообщения об отказе — ограничим права в обработчиках
        return await handler(event, data)