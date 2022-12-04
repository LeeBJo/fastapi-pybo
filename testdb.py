from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)


def get_db():                      # db 세션 객체를 리턴하는 제너레이터인 get_db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   # 함수는 사용한 세션을 컨넥션 풀에 반환하는 함수이다. (세션을 종료하는 것으로 착각하지 말자.)