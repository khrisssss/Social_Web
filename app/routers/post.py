from fastapi import APIRouter
from pydantic import BaseModel
from database.database import get_connection

router = APIRouter(prefix="/posts", tags=["Posts"])


class CreatePost(BaseModel):
    user_id: int
    content: str


@router.post("/")
def create_post(post: CreatePost):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user WHERE id = ?", (post.user_id,))
    cursor.fetchone()

    cursor.execute(
        "INSERT INTO message (creator_id, content) VALUES (?, ?)",
        (post.user_id, post.content),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Post created successfully",
        "post_id": post_id,
        "user_id": post.user_id,
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
    cursor.execute("SELECT * FROM message ")
    everything_post = cursor.fetchall()
    conn.commit()
    conn.close()
    return  [dict(post) for post in everything_post]
