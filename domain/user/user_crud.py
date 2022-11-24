from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from testModel import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   alarmAccepted=user_create.alarmAccepted)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):        # 중복 아이디, 이메일 사전 방지
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db:Session, username: str):                            # 사용자명으로 사용자 모델 객체를 리턴하는 get_user 함수
    return db.query(User).filter(User.username == username).first()