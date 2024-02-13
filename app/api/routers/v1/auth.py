from models.schemas import UserLogin
from database import Session, get_db
from auth.security import pwd_context
from models.models import User
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post("/login")
async def login(
    user: UserLogin, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    Authenticates a user via email and password, generates a JWT access token
    with aggregated permissions from the user's groups, and returns the token.

    Parameters:
    - user: UserLogin schema containing the user's email and password.
    - Authorize: AuthJWT dependency for handling JWT operations.
    - db: Database session dependency from get_db.

    Raises:
    - HTTPException: With status code 401 if the email or password is incorrect.

    Returns:
    - A JSON response containing the JWT access token for the authenticated user.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Aggregate permissions from all groups the user belongs to
    permissions = set()
    for group in db_user.groups:
        permissions.update(group.permissions)

    access_token = Authorize.create_access_token(
        subject=db_user.id, user_claims={"permissions": list(permissions)}
    )
    return {"access_token": access_token}
