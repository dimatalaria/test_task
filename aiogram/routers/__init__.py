__all__ = ("router", )

from aiogram import Router

from .admin_handlers import router as admin_router
from .commands import router as commands_router
from .command import router as command_router

router = Router(name=__name__)

router.include_router(commands_router)
router.include_router(admin_router)
router.include_router(command_router)