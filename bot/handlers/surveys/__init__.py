from aiogram import Router

from .change_role import router as change_role_survey_router

router = Router(name=__name__)
router.include_routers(change_role_survey_router)
