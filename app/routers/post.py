from fastapi import APIRouter
from pydantic import BaseModel
from database.database import get_connection
import datetime

router = APIRouter(prefix="/posts", tags=["Posts"])


class CreatePost(BaseModel):
    user_id: int
    content: str
    datetime: datetime.datetime


@router.post("/")
def create_post(post: CreatePost):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user WHERE id = ?", (post.user_id,))
    cursor.fetchone()

    cursor.execute(
        "INSERT INTO message (creator_id, content, timestamp) VALUES (?, ?, ?)",
        (post.user_id, post.content, post.timestamp),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Post created successfully",
        "post_id": post_id,
        "user_id": post.user_id,
        "content": post.content,
        "timestamp": post.timestamp,
    }


class creator(BaseModel):
    id: int


@router.get("/user/{user_id}")
def get_user_post(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    # get all the post from this specific user
    cursor.execute("SELECT * from message WHERE creator_id = ?", (user_id,))
    all_post = cursor.fetchall()
    print("list: ", all_post)
    conn.commit()
    conn.close()
    return {
        "user_id": user_id,
        "posts": [dict(post) for post in all_post]
    }


@router.get("/")
def get_all_post():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM message ")
    everything_post = cursor.fetchall()
    conn.commit()
    conn.close()
    return [dict(post) for post in everything_post]


class Likes(BaseModel):
    post_id: int
    user_id: int

@router.post("/like/{post_id}")
def like_post(likes: Likes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO like (user_id, message_id) VALUES (?, ?)",
        (likes.user_id, likes.post_id),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Liked successfully",
        "post_id": likes.post_id,
        "user_id": likes.user_id,
    }

@router.post("/likes/{post_id}")
def count_likes(post_id: int):
    #print("post id: ", likes.post_id)   
    conn = get_connection()
    cursor = conn.cursor()
    #print("post id: ", likes.post_id)
    cursor.execute(
        "SELECT count(*) FROM like WHERE message_id = ?", (post_id,))
    like_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"post_id": post_id, "likes": like_count}


class Comment (BaseModel):
    content: str
    user_id: int 
    post_id: int 


@router.post("/comment/{post_id}/comments")
def comment_post(post_id: int, comment: Comment): 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comment (content, user_id, message_id) VALUES (?, ?, ?)",
        (comment.content, comment.user_id, post_id),
    )
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    return {
        "message": "Commented successfully",
        "comment_id": comment_id,
        "post_id": post_id,
        "user_id": comment.user_id,
        "content": comment.content
    }
