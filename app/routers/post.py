from fastapi import APIRouter, HTTPException
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

