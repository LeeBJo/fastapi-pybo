from datetime import datetime

from domain.recommend_diet_question.r_question_schema import RQuestionCreate, RQuestionUpdate
from testModel import RecommendQuestion, User, RecommendAnswer
from sqlalchemy.orm import Session


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = '', is_admin: bool = False, user_id: int = 0 ):
    question_list = db.query(RecommendQuestion).filter(RecommendQuestion.user_id == user_id)
    print(question_list)
    if is_admin:
        question_list = db.query(RecommendQuestion)
    '''
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(RecommendAnswer.question_id, RecommendAnswer.content, User.username) \
            .outerjoin(User, RecommendAnswer.user_id == User.id).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, sub_query.c.question_id == RecommendQuestion.id) \
            .filter(RecommendQuestion.subject.ilike(search) |  # 질문제목
                    RecommendQuestion.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )'''
    print("!!!!!!!!!!!!!!!!!3")
    total = question_list.distinct().count()
    question_list = question_list.order_by(RecommendQuestion.create_date.desc()) \
        .offset(skip).limit(limit).distinct().all()
    print(question_list)    #test
    print(total)        #test
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)
    # 프론트에서 정보를 못 보냄


def get_question(db: Session, question_id: int):
    question = db.query(RecommendQuestion).get(question_id)
    return question


def create_question(db: Session, question_create: RQuestionCreate, user: User):
    db_question = RecommendQuestion(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()


def update_question(db: Session, db_question: RecommendQuestion,
                    question_update: RQuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: RecommendQuestion):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: RecommendQuestion, db_user: User):
    db_question.voter.append(db_user)
    db.commit()