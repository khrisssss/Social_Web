from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.database import get_connection
import datetime
from typing import Optional

from utils.auth_utils import get_current_user
from utils.comments_service import  get_comments_for_post


router = APIRouter(prefix="/posts", tags=["Posts"])


class CreatePost(BaseModel):
    content: str


@router.post("/")
def create_post(post: CreatePost, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO message (creator_id, content) VALUES (?, ?)",
        (current_user["id"], post.content),)

    conn.commit()
    post_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Post created successfully",
        "post_id": post_id,
        "created_by": current_user["username"],
        "content": post.content,
        "created_at": datetime.datetime.now().isoformat()
    }


class creator(BaseModel):
    id: int


@router.get("/user/{user_id}")
def get_user_posts(user_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM message
        WHERE creator_id = ?
        AND id NOT IN (SELECT message_id FROM response)
    """, (user_id,))

    posts = [dict(post) for post in cursor.fetchall()]
    conn.close()

    for post in posts:
        post["comments"] = get_comments_for_post(post["id"])

    return {"user_id": user_id, "posts": posts}


@router.get("/")
def get_all_post(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM message
        WHERE id NOT IN (SELECT message_id FROM response)
        ORDER BY creation_date DESC
    """)

    posts = [dict(post) for post in cursor.fetchall()]
    conn.close()

    for post in posts:
        post["comments"] = get_comments_for_post(post["id"])

    return posts

class Likes(BaseModel):
    post_id: int

@router.post("/like/{post_id}")
def like_post(likes: Likes, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO like (user_id, message_id) VALUES (?, ?)",
        (current_user["id"], likes.post_id),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Liked successfully",
        "post_id": likes.post_id,
        "user_id": current_user["id"],
    }

@router.get("/likes/")
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
    parent_id: Optional[int] = None
    

@router.post("/{post_id}/comment")
def comment_post(post_id: int, comment: Comment, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    actual_parent = comment.parent_id if comment.parent_id else post_id
    cursor.execute(
        "INSERT INTO message (content, creator_id) VALUES (?, ?)",
        (comment.content, current_user["id"]),)

    comment_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO response (message_id, parent_id) VALUES (?, ?)",
        (comment_id, actual_parent),)
    conn.commit()
    conn.close()

    return {
        "id": comment_id,
        "content": comment.content,
        "user_id": current_user["id"],
        "parent_id": actual_parent,
        "created_at": datetime.datetime.now().isoformat(),
        "replies": []
    }




