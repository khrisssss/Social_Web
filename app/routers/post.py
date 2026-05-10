from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.database import get_connection
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


class CreatePost(BaseModel):
    content: str


@router.post("/")
def create_post(post: CreatePost, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO message (creator_id, content) VALUES (?, ?)",
        (current_user["id"], post.content),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Post created successfully",
        "post_id": post_id,
        "author": current_user["username"],
        "content": post.content,
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
    cursor.execute("""
        SELECT message.id, message.content, message.image,
               user.pseudo AS author
        FROM message
        JOIN user ON message.creator_id = user.id
        ORDER BY message.id DESC
    """)
    everything_post = cursor.fetchall()
    conn.close()
    return [dict(post) for post in everything_post]
