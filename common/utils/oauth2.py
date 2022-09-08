from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user import models, schemas
from common.db import get_db

from common import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



JWT_SECRET_KEY = config.JWT_SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # print(token)
        # payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        payload = jwt.decode(token, JWT_SECRET_KEY)
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        # print(e)
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme),
                     db: AsyncSession = Depends(get_db)):
    async with db as s:
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                              detail=f"could not vallidate credentials",
                                              headers={'Authorization': "Bearer"})
        token = verify_access_token(token, credentials_exception)

        sql = select(models.User).where(models.User.id == token.id)
        result = s.execute(sql)
        return result.scalars().first()
