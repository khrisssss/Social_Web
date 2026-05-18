from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.database import get_connection
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/followers", tags=["Followers"])

class follow(BaseModel):
    following_id: int

@router.post("/")
def follow_user(follow_data: follow, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM follower WHERE follower_id = ? AND following_id = ?",
        (current_user["id"], follow_data.following_id),
    )
    existing_follow = cursor.fetchone()
    if existing_follow:
        conn.close()
        return {"message": "Already following this user"}
    
    if current_user["id"] == follow_data.following_id:
        conn.close()
        return {"message": "You cannot follow yourself"}

    cursor.execute(
        "INSERT INTO follower (follower_id, following_id) VALUES (?, ?)",
        (current_user["id"], follow_data.following_id),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Followed successfully",
        "follower_id": current_user["id"],
        "following_id": follow_data.following_id,
    }

@router.post("/count_followers/")
def count_followers(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT count(*) FROM follower WHERE following_id = ?", (user_id,))
    follower_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"user_id": user_id, "followers": follower_count}








