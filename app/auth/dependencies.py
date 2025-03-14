from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth_utils import SECRET_KEY, ALGORITHM
from app.config.database import get_db
from sqlalchemy import text

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de credenciais inválido ou ausente",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        try:
            user_id_int = int(user_id)
        except ValueError:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = await db.execute(
        text("SELECT * FROM users WHERE id = :id LIMIT 1"), 
        {"id": user_id_int} 
    )
    
    user_row = user.fetchone()
    if not user_row:
        raise credentials_exception

    return user_row
