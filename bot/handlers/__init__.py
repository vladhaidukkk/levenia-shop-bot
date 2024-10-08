from aiogram import Router

from .buttons import router as buttons_router
from .commands import router as commands_router
from .surveys import router as surveys_router

router = Router(name=__name__)
router.include_routers(surveys_router, commands_router, buttons_router)
