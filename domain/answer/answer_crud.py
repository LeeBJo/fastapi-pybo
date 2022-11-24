from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from testModel import Question, Answer, User

# crud : db와 연산

def create_answer(db: Session, question: Question,
                  answer_create: AnswerCreate, user:User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user)   # user: 글쓴이 정보
    db.add(db_answer)
    db.commit()

def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def update_answer(db: Session, db_answer:Answer,
                 answer_update:AnswerUpdate):
    db_answer.content = answer_update.content       # 내용 업데이트
    db_answer.modify_date = datetime.now()          # 수정 날짜 업데이트
    db.add(db_answer)                               # 업데이트
    db.commit()

def delete_answer(db: Session, db_answer:Answer):
    db.delete(db_answer)
    db.commit()