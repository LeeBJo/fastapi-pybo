from datetime import datetime

from sqlalchemy.orm import Session

from domain.recommend_diet_answer.r_answer_schema import RAnswerCreate, RAnswerUpdate
from testModel import Question, Answer, User


def create_answer(db: Session, question: Question,
                  answer_create: RAnswerCreate, user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)


def update_answer(db: Session, db_answer: Answer,
                  answer_update: RAnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()


def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()