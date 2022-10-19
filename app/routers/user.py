from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from ..schemas import user_schema
from ..database import get_db
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: user_schema.UserRequest, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unable to create a user")
    db.refresh(new_user)
    return new_user


@router.get(
    "/{id}",
    response_model=user_schema.UserResponse
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} was not found.")
    return user
