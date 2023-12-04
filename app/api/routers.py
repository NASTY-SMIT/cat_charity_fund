from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    donation_router,
    user_router)
from app.constants import PREFIX_CHARITY_PROJECT, PREFIX_DONATION

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix=PREFIX_CHARITY_PROJECT, tags=['Charity Projects'])
main_router.include_router(donation_router, prefix=PREFIX_DONATION, tags=['Donations'])
main_router.include_router(user_router)
