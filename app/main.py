from fastapi import FastAPI, Request
from api.routers.v1 import router as api_router_v1
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from auth.config import get_config

app = FastAPI()

app.include_router(api_router_v1, prefix="/api/v1")


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
