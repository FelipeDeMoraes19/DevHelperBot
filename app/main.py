from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import chat

app = FastAPI(title="DevHelperBot API", version="1.0.0")

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.on_event("startup")
async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health_check():
    return {"status": "active", "version": app.version}