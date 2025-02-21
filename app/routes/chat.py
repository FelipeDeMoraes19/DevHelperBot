from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated
from pydantic import BaseModel
from app.nlp.processor import NLPProcessor
from app.models.conversation import Conversation
from app.config.database import AsyncSessionLocal, get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
nlp = NLPProcessor()

class ChatRequest(BaseModel):
    user_input: str
    session_id: str

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        processed = nlp.process_input(request.user_input)
        
        new_conversation = Conversation(
            session_id=request.session_id,
            user_input=request.user_input,
            bot_response=processed["response"],
            code_example=processed.get("code_example", "")
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