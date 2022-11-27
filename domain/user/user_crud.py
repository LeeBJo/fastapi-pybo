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

def get_user_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''): #skip:조회데이터의 시작위치, limit:시작위치로부터 가져올 데이터 건수
    user_list = db.query(User)
    if keyword:
        user_list = db.query(User).filter(User.username==keyword)
    total = user_list.count()
    user_list = user_list.order_by(User.id.desc()) \
        .offset(skip).limit(limit).all()
    return total, user_list             # (전체 건수, 페이징 적용된 질문 목록)

def get_existing_user(db: Session, user_create: UserCreate):        # 중복 아이디, 이메일 사전 방지
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db:Session, username: str):                            # 사용자명으로 사용자 모델 객체를 리턴하는 get_user 함수
    return db.query(User).filter(User.username == username).first()