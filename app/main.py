from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models
from .database import get_db, engine
from . import schemas
from .utils import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my API app!"}


@app.get(
    "/posts",
    response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get(
    "/posts/{id}",
    response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' was not found")
    return post


@app.post(
    "/create_post",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse)
def create_post(post: schemas.PostRequest, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.delete()
    db.commit()


@app.put(
    "/posts/{id}",
    response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostRequest, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.update(post.dict())
    db.commit()
    updated_post = post_query.first()
    return updated_post


@app.post(
    "/create_user",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserRequest, db: Session = Depends(get_db)):
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


@app.get(
    "/users/{id}",
    response_model=schemas.UserResponse
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} was not found.")
    return user
