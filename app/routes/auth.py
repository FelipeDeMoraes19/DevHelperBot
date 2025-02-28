from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from app.models.user import User
from app.auth.auth_utils import (
    create_access_token,
    get_password_hash,
    verify_password,
    SECRET_KEY,
    ALGORITHM
)
from app.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
        text("SELECT * FROM users WHERE email = :email OR username = :username LIMIT 1"),
        {"email": user_data.email, "username": user_data.username}
    )
    if existing_user.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Email ou username já em uso."
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"msg": "Usuário criado com sucesso", "user_id": new_user.id}


@router.post("/login")
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await db.execute(
        text("SELECT * FROM users WHERE email = :email LIMIT 1"),
        {"email": login_data.email}
    )
    user_row = user.fetchone()
    if not user_row:
        raise HTTPException(
            status_code=400,
            detail="Email não encontrado."
        )

    if not verify_password(login_data.password, user_row.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Senha incorreta."
        )

    access_token = create_access_token({"sub": str(user_row.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_row.id,
        "username": user_row.username
    }
