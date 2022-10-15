import time
from random import randint
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from .creds import PG_USERNAME, PG_PASSWORD, PG_HOSTNAME, PG_DB_NAME

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host=PG_HOSTNAME, database=PG_DB_NAME,
                                user=PG_USERNAME, password=PG_PASSWORD,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to DB successful!")
        break
    except Exception as error:
        print("Connection to DB failed! Error:", error)
        time.sleep(1)


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my API app!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"All posts": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", vars=(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    return {f"The post with id={id}": post}


@app.post("/create_posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *",
                   vars=(post.title, post.content, post.is_published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Successfully created the post": new_post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", vars=(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    return {"Successfully deleted the post": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *",
                   vars=(post.title, post.content, post.is_published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found")
    return {"Successfully updated the post": updated_post}
