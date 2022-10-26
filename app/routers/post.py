from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models
from ..schemas import post_schema
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get(
    "/all",
    response_model=List[post_schema.PostResponse]
)
def get_posts(
        db: Session = Depends(get_db)):
    """A guest can see all published posts created by any users"""
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.is_published == True) \
        .group_by(models.Post.id).all()
    return posts


@router.get(
    "/my",
    response_model=List[post_schema.PostResponse])
def get_my_posts(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)
):
    """A user can see all his post"""
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.user_id == current_user.id).group_by(models.Post.id) \
        .all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You don't have any posts")
    return posts


@router.get(
    "/my/draft",
    response_model=List[post_schema.PostResponse])
def get_my_draft_posts(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)
):
    """A user can see all his draft (unpublished) post"""
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.user_id == current_user.id, models.Post.is_published == False) \
        .group_by(models.Post.id) \
        .all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You don't have any unpublished posts")
    return posts


@router.get(
    "/{id}",
    response_model=post_schema.PostResponse)
def get_post(
        id: int,
        db: Session = Depends(get_db)):
    """A guest can see any exact post created by any user (only published)"""
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.id == id, models.Post.is_published == True) \
        .group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=post_schema.PostResponseBase)
def create_post(
        post: post_schema.PostRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    """A user can create a post"""
    new_post = models.Post(**post.dict(), user_id=current_user.id)
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
    """A user can delete his posts"""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to delete this post.")
    post_query.delete()
    db.commit()


@router.put(
    "/{id}",
    response_model=post_schema.PostResponseBase)
def update_post(
        id: int,
        post: post_schema.PostRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    """A user can update his posts"""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post_data = post_query.first()

    if old_post_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    if old_post_data.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to update this post.")

    new_post_data = post.dict()
    new_post_data.update({"user_id": current_user.id})
    post_query.update(new_post_data)
    db.commit()
    updated_post = post_query.first()
    return updated_post
