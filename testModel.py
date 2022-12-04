from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from testdb import Base

question_voter = Table(
    'question_voter',               # 테이블 이름
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "question"                              # 테이블 이름

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)            # String = 글자 수 제한 텍스트
    content = Column(Text, nullable=False)              # Text   = 글자 수 제한 없는 텍스트
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)       # 수정일
    voter = relationship('User', secondary=question_voter, backref='question_voters')
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)     # 글쓴이, user 모델을 question 모델과 연결시키기 위한 속성
    user = relationship("User", backref="question_users")               # Question 모델에서 User 모델을 참조하기 위한 속성


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    modify_date = Column(DateTime, nullable=True)           # 수정일

    # 글쓴이
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)     # unique : 같은 값을 저장할 수 없다\
    alarmAccepted = Column(Boolean, default=False)
    authority = Column(Boolean, default=False)
    modify_date = Column(DateTime, nullable=True)  # 수정일

class HealthInfo(Base):
    __tablename__ = "health_info"

    id = Column(Integer, primary_key=True)
    subject = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    create_date = Column(DateTime, nullable=False)

class RecommendQuestion(Base):
    __tablename__ = "recommend_question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)

class RecommendAnswer(Base):
    __tablename__ = "recommend_answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("recommend_question.id"))
    question = relationship("RecommendQuestion", backref="recommend_answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)

# DB 테이블 추가 시
# alembic revision --autogenerate
# alembic upgrade head
# 필수