import datetime

from pydantic import BaseModel, validator   # validator : 빈칸 입력 방지

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    subject: str                        # nullable 한 경우 subject: str | None = None
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []          # 답변 목록
    user: User | None
    modify_date: datetime.datetime | None = None    # 수정일
    voter: list[User] = []

    class Config:
        orm_mode = True

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionUpdate(QuestionCreate):       # QuestionCreate class 상속
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int

#만약 Question 스키마에서 content 항목을 제거한다면 질문 목록 API의 출력 항목에도 content 항목이 제거될 것이다.
# 이 때, 실제 리턴되는 _question_list를 수정할 필요가 없다. 단지 스키마에서만 제외하면 되니 편리하다.