from fastapi import APIRouter
from pydantic import BaseModel
from database.database import get_connection

router = APIRouter(prefix="/followers", tags=["Followers"])

class follow(BaseModel):
    follower_id: int
    following_id: int

@router.post("/")
def follow_user(follow_data: follow):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO follower (follower_id, following_id) VALUES (?, ?)",
        (follow_data.follower_id, follow_data.following_id),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Followed successfully",
        "follower_id": follow_data.follower_id,
        "following_id": follow_data.following_id,
    }

@router.post("/count_followers/{user_id}")
def count_followers(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT count(*) FROM follower WHERE following_id = ?", (user_id,))
    follower_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"user_id": user_id, "followers": follower_count}








