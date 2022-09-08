from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.db import get_db
from common.utils import oauth2
from app.user import models
from app.user.schemas import Token
from common.utils import verify

router = APIRouter()


@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    async with db as s:
        sql = select(models.User).where(models.User.email == user_credentials.username)
        db_user = (await s.execute(sql)).scalar_one_or_none()


    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")

    if not verify(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")

# create a token, and return it
    access_token = oauth2.create_access_token(data={'user_id': db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}





