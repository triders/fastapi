from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    is_published: Optional[bool]


@app.get("/")
def root():
    return {"message": "Welcome to my API app!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"All posts": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    return {f"The post with id={id}": post}


@app.post("/create_posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Successfully created the post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.delete()
    db.commit()


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    post_query.update(post.dict())
    db.commit()
    updated_post = post_query.first()
    return {"Successfully updated the post": updated_post}
