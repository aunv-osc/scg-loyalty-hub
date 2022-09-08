from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.user import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app.user.schemas import UserOut
from common.db import get_db
from common import utils
from common.utils import validate_email


async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    if user.email and not validate_email(user.email):
        raise Exception('Email is invalid!')

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    async with db as s:
        query = insert(models.User).values(email=user.email, password=user.password)
        await s.execute(query)

        sql = select(models.User).filter(models.User.email == user.email)
        db_user = (await s.execute(sql)).scalars().unique().one()
        await s.commit()

    db_user_serialize_data = db_user.as_dict()
    return UserOut(**db_user_serialize_data)

async def get_users(id: int, db: AsyncSession = Depends(get_db)):

    async with db as s:
        sql = select(models.User).where(models.User.id == id)
        db_user = (await s.execute(statement=sql))

    return db_user.scalar_one_or_none()
