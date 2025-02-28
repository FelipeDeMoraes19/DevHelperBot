from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import chat
from app.routes import auth
from app.models import conversation, feedback 
from app.routes import feedback as feedback_routes
import os  

app = FastAPI(title="DevHelperBot API", version="1.0.0")

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(auth.router)
app.include_router(feedback_routes.router, prefix="/api/v1", tags=["Feedback"]) 

@app.on_event("startup")
async def startup_db():
    if os.getenv("ENV") != "testing":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health_check():
    return {"status": "active", "version": app.version}
