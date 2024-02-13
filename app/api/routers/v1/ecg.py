from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks, APIRouter
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ecg.processors import process_ecg
from uuid import UUID
import models.schemas as schemas
import models.models as models
from auth.permissions import PermissionChecker
from database import get_db

router = APIRouter()


@router.post("/ecgs")
async def create_ecg(
    background_tasks: BackgroundTasks,
    ecg_data: schemas.ECGCreate,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    permissions: bool = Depends(PermissionChecker(["ecg:create"])),
) -> dict:
    """
    Creates an ECG record and schedules it for processing.

    Parameters:
        background_tasks (BackgroundTasks): FastAPI's background task manager.
        ecg_data (schemas.ECGCreate): The ECG data to create.
        Authorize (AuthJWT): AuthJWT dependency for JWT operations.
        db (Session): Database session dependency from get_db.
        permissions (bool): PermissionChecker dependency, verifying user permissions.

    Raises:
        HTTPException: With status code 400 if there's an error creating the ECG.

    Returns:
        dict: A message indicating successful creation and the ECG's ID.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    try:
        new_ecg = models.ECG(user_id=user_id)
        db.add(new_ecg)
        db.flush()

        for lead_data in ecg_data.leads:
            new_lead = models.Lead(ecg_id=new_ecg.id, **lead_data.dict())
            db.add(new_lead)
            db.commit()
        # Schedule the background task after the commit
        background_tasks.add_task(process_ecg, new_ecg.id)
        return {"message": f"ECGs created successfully", "ecg_id": f"{str(new_ecg.id)}"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating ECG: {str(e)}")


@router.get("/ecgs/{ecg_id}", response_model=schemas.ECGOut)
async def get_ecg(
    ecg_id: UUID,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    permissions: bool = Depends(PermissionChecker(["ecg:read"])),
) -> schemas.ECGOut:
    """
    Retrieves an ECG record by its ID.

    Parameters:
        ecg_id (UUID): The ID of the ECG to retrieve.
        Authorize (AuthJWT): AuthJWT dependency for JWT operations.
        db (Session): Database session dependency from get_db.
        permissions (bool): PermissionChecker dependency, verifying user permissions.

    Raises:
        HTTPException: With status code 404 if the ECG is not found.
        HTTPException: With status code 204 if the ECG has not been processed yet.

    Returns:
        schemas.ECGOut: The retrieved ECG record.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    # Fetch the ECG, ensuring it belongs to the requesting user
    ecg = (
        db.query(models.ECG)
        .filter(models.ECG.id == ecg_id, models.ECG.user_id == user_id)
        .first()
    )
    if not ecg:
        raise HTTPException(status_code=404, detail="ECG not found")
    if not ecg.processed:
        raise HTTPException(
            status_code=204, detail="ECG not processed yet, please try again later"
        )
    return ecg
