from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..utils import verify_password
from ..oauth2 import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials.")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials.")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
