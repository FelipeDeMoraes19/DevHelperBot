from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated
from pydantic import BaseModel
from app.nlp.processor import NLPProcessor
from app.models.conversation import Conversation
from app.config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from sqlalchemy import text

router = APIRouter()
nlp = NLPProcessor()


class ChatRequest(BaseModel):
    user_input: str
    session_id: str


@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        processed = nlp.process_input(request.user_input)

        new_conversation = Conversation(
            session_id=request.session_id,
            user_input=request.user_input,
            bot_response=processed["response"],
            code_example=processed.get("code_example", ""),
            user_id=current_user.id
        )

        db.add(new_conversation)
        await db.commit()

        return {
            "response": processed["response"],
            "code_example": processed.get("code_example", ""),
            "intent": processed["intent"]
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    rows = await db.execute(
        text("SELECT * FROM conversations WHERE user_id = :user_id ORDER BY id DESC"), 
        {"user_id": current_user.id}
    )

    convos = rows.fetchall()

    result = []
    for row in convos:
        result.append({
            "id": row.id,
            "session_id": row.session_id,
            "user_input": row.user_input,
            "bot_response": row.bot_response,
            "code_example": row.code_example,
            "timestamp": row.timestamp.isoformat() if row.timestamp else None
        })
    return result
