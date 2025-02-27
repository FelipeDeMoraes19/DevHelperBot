from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.config.database import get_db
from app.models.feedback import Feedback
from app.models.conversation import Conversation

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackCreate(BaseModel):
    conversation_id: int
    rating: int 

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_feedback(
    data: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    conversation = await db.execute(
        "SELECT * FROM conversations WHERE id=:id AND user_id=:user_id",
        {"id": data.conversation_id, "user_id": current_user.id}
    )
    row = conversation.fetchone()
    if not row:
        raise HTTPException(
            status_code=404, detail="Conversation not found or doesn't belong to you"
        )

    new_feedback = Feedback(
        conversation_id=data.conversation_id,
        rating=data.rating
    )
    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    return {"msg": "Feedback saved", "feedback_id": new_feedback.id}

@router.get("/")
async def list_feedback(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    sql = """
    SELECT f.id, f.conversation_id, f.rating, f.created_at
    FROM feedback f
    JOIN conversations c ON c.id = f.conversation_id
    WHERE c.user_id = :user_id
    ORDER BY f.id DESC
    """
    results = await db.execute(sql, {"user_id": current_user.id})
    rows = results.fetchall()

    feedback_list = []
    for row in rows:
        feedback_list.append({
            "id": row.id,
            "conversation_id": row.conversation_id,
            "rating": row.rating,
            "created_at": row.created_at.isoformat() if row.created_at else None
        })
    return feedback_list
