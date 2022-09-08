from typing import Optional
from pydantic import BaseModel
from datetime import datetime



# for response Model class
class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    #
    # class Config:
    #     allow_population_by_field_name = True


# User
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None