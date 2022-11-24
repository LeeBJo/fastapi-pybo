import datetime

from pydantic import BaseModel, validator
from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None

    class Config:
        orm_mode = True

class AnswerUpdate(AnswerCreate):
    answer_id:int

class AnswerDelete(BaseModel):
    answer_id:int

# Answer 스키마는 출력으로 사용할 답변 1건(단 건)을 의미한다