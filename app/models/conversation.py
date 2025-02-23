from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50))
    user_input = Column(String(500))
    bot_response = Column(String(500))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    code_example = Column(String(2000))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", backref="conversations")
