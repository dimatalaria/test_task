__all__ = ("router", )

from aiogram import Router

from .base_commands import router as base_commands_router
from .user_commands import router as user_commands_router
from .user_tasks import router as user_tasks_router
from .task_comments import router as comment_task_router

router = Router(name=__name__)

router.include_router(base_commands_router)
router.include_router(user_commands_router)
router.include_router(user_tasks_router)
router.include_router(comment_task_router)