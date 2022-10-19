from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app import schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get(
    "/",
    response_model=List[schemas.PostResponse])
def get_posts(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get(
    "/{id}",
    response_model=schemas.PostResponse)
def get_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse)
def create_post(
        post: schemas.PostRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.delete()
    db.commit()


@router.put(
    "/{id}",
    response_model=schemas.PostResponse)
def update_post(
        id: int,
        post: schemas.PostRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.update(post.dict())
    db.commit()
    updated_post = post_query.first()
    return updated_post
