import datetime

from pydantic import BaseModel, validator
from domain.user.user_schema import User


class RAnswerCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class RAnswer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None

    class Config:
        orm_mode = True


class RAnswerUpdate(RAnswerCreate):
    answer_id: int


class RAnswerDelete(BaseModel):
    answer_id: int
