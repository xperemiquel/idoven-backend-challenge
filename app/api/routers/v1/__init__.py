from fastapi import APIRouter
from . import ecg, users, auth

router = APIRouter()

router.include_router(ecg.router, tags=["ecgs"])
router.include_router(auth.router, tags=["auth"])
router.include_router(users.router, tags=["users"])
