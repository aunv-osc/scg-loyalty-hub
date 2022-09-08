from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from common.db import get_db
from app.user import schemas, models, services

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_user(user, db)


@router.get("/{id}", response_model=schemas.UserOut)
async def get_users(id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_users(id, db)