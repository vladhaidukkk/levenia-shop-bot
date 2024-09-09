from aiogram import Router

from .client import router as client_buttons_router
from .manager import router as manager_buttons_router

router = Router(name=__name__)
router.include_routers(manager_buttons_router, client_buttons_router)
