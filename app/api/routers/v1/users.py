from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import models.schemas as schemas
import models.models as models
from auth.permissions import PermissionChecker
from database import get_db
from auth.security import get_password_hash

router = APIRouter()


@router.post("/users")
async def create_ecgs_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    permissions: bool = Depends(PermissionChecker(["user:create"])),
):
    """
    Creates a new user with ECG Operator permissions.

    Parameters:
        user (schemas.UserCreate): User creation schema with email and password.
        db (Session): Database session dependency from get_db.
        permissions (bool): PermissionChecker dependency, verifying user permissions to create users.

    Raises:
        HTTPException: With status code 400 if the email is already registered.

    Returns:
        dict: success or failure message
    """
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash user password
    hashed_password = get_password_hash(user.password)

    group = (
        db.query(models.PermissionGroup)
        .filter(models.PermissionGroup.name == "ECGOperator")
        .first()
    )

    # Create new user instance
    db_user = models.User(email=user.email, password=hashed_password, groups=[group])

    # Add new user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}
