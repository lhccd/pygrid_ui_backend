import io
import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse

from app import crud, models, schemas
from starlette.responses import StreamingResponse

from ....models.pdf import PDFObject
from ....schemas.user import UserProfile, PendingUser, ActiveUser, DeniedUser, UserDetail, UserUpdate, UserBudget, UserUpdateWithPassword
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.put("/update-password", response_model=schemas.User)
def update_user_password(
        *,
        db: Session = Depends(deps.get_db),
        current_password: str = Body(None),
        password: str = Body(None),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    user = crud.user.authenticate(
        db, email=current_user.email, password=current_password
    )
    if user:
        user_in.password = password
    else:
        raise HTTPException(
            status_code=400,
            detail="Current password could not be confirmed. Please check again."
        )
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.put("/update-profile-password", response_model=schemas.User)
def update_user_password(
        *,
        db: Session = Depends(deps.get_db),
        current_password: str = Body(None),
        password: str = Body(None),
        full_name: str = Body(...),
        website: str = Body(...),
        email: EmailStr = Body(...),
        institution: str = Body(...),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdateWithPassword(**current_user_data)
    user = crud.user.authenticate(
        db, email=current_user.email, password=current_password
    )
    if user:
        user_in.password = password
        user_in.full_name = full_name
        user_in.website = website
        user_in.email = email
        user_in.institution = institution
    else:
        raise HTTPException(
            status_code=400,
            detail="Current password could not be confirmed. Please check again."
        )
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/user-detail", response_model=UserDetail, responses={200: {"Success": "User Fetched Successfully"}})
def get_user_by_id(
        *,
        db: Session = Depends(deps.get_db),
        user_email: EmailStr,
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    user = crud.user.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user


@router.get("/user-daa", responses={200: {"content": {"application/pdf": {}}}})
def get_user_daa_by_id(
        *,
        db: Session = Depends(deps.get_db),
        user_email: EmailStr,
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    pdf_obj = crud.user.get_pdf_by_email(db, email=user_email)

    return StreamingResponse(io.BytesIO(pdf_obj.binary), media_type="application/pdf")


@router.post("/open", response_model=schemas.User)
def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(...),
        website: str = Body(None),
        institution: str = Body(None),
        budget: float = Body(None),
) -> Any:
    """
    Create new user without daa requirement
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name, website=website,
                                 institution=institution, budget=budget, allocated_budget=budget, created_at=datetime.now())
    user = crud.user.create_with_no_daa(db, obj_in=user_in)
    return user


@router.post("/open-daa", response_model=schemas.User)
async def create_user_daa(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(...),
        website: str = Body(None),
        institution: str = Body(None),
        budget=0.0,
        daa_pdf: UploadFile = File(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    pdf_file = await daa_pdf.read()
    pdf_obj = models.pdf.PDFObject(binary=pdf_file)
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name, daa_pdf=pdf_obj.binary,
                                 website=website,
                                 institution=institution, budget=budget, allocated_budget=budget, created_at=datetime.now())
    user = crud.user.create_with_daa(db, obj_in=user_in)
    return user


@router.get("/user-profile", response_model=UserProfile)
def read_user_by_id(
        current_user: models.User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get_user_profile(db, id=current_user.id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user does not exist"
        )
    return user


@router.put("/", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        email: EmailStr = Body(...),
        full_name: str = Body(...),
        website: str = Body(None),
        institution: str = Body(None),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=current_user.id)
    user_in = UserProfile(full_name=full_name, email=email, website=website, institution=institution)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update_profile(db, db_obj=user, obj_in=user_in)
    return user

@router.put("/update-budget", response_model=UserBudget)
def update_budget(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        user_email: EmailStr,
        budget: float = Body(...),
) -> Any:
    """
    Update a user's budget.
    """
    user = crud.user.get_by_email(db, email=user_email)
    user_in = UserBudget(budget=budget)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update_budget(db, db_obj=user, obj_in=user_in)
    return user


@router.put("/accept", response_model=schemas.User)
def accept_user(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        user_email: EmailStr = Body(...),
):
    user = crud.user.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system"
        )
    user_in = UserUpdate(status="accepted", added_by=current_user.full_name)
    return crud.user.update_profile(db, db_obj=user, obj_in=user_in)


@router.put("/deny", response_model=schemas.User)
def deny_user(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        user_email: EmailStr = Body(...),
):
    user = crud.user.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system"
        )
    user_in = UserUpdate(status="denied")
    return crud.user.update_profile(db, db_obj=user, obj_in=user_in)



@router.delete("/")
def delete_user(
        current_user: models.User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db),
) -> None:
    """
    Here deleting only current user - needs adjustment
    + deleting roles permissions etc
    """
    user_email = current_user.email
    try:
        crud.user.delete(db, email=user_email)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail="Error"
        )


@router.get("/accepted-users", response_model=List[ActiveUser])
def get_accepted_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve Accepted Users.
    """
    # fetch users with a status = accepted/pending/denied
    users = crud.user.get_users_by_status(db, skip=skip, limit=limit)
    return users


@router.get("/pending-users", response_model=List[ActiveUser])
def get_pending_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve Pending Users.
    """
    # fetch users with a status = active/pending/denied
    users = crud.user.get_users_by_status(db, skip=skip, limit=limit, status="pending")
    return users


@router.get("/denied-users", response_model=List[ActiveUser])
def get_denied_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve Denied Users.
    """
    # fetch users with a status = active/pending/denied
    users = crud.user.get_users_by_status(db, skip=skip, limit=limit, status="denied")
    return users