from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, domain, upgradeRequests, dataRequests

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(domain.router, prefix="/domain", tags=["domain"])
api_router.include_router(upgradeRequests.router, prefix="/upgrade-requests", tags=["upgrade-requests"])
api_router.include_router(dataRequests.router, prefix="/data-requests", tags=["data-requests"])

