from pydantic import BaseModel
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    authjwt_secret_key: str = "secret_key_here"
    authjwt_access_token_expires: timedelta = timedelta(minutes=90)


@AuthJWT.load_config
def get_config():
    return Settings()
