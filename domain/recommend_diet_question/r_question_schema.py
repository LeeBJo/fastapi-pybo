import datetime

from pydantic import BaseModel, validator

from domain.recommend_diet_answer.r_answer_schema import RAnswer
from domain.user.user_schema import User


class RQuestion(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[RAnswer] = []
    user: User | None
    modify_date: datetime.datetime | None = None

    class Config:
        orm_mode = True


class RQuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class RQuestionList(BaseModel):
    total: int = 0
    question_list: list[RQuestion] = []


class RQuestionUpdate(RQuestionCreate):
    question_id: int


class RQuestionDelete(BaseModel):
    question_id: int