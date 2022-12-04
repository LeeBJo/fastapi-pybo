from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

from testModel import User
from testdb import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

config = Config('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)

@router.get("/list", response_model=user_schema.UserList)   # 리턴타입 = user_schema의 UserList
def user_list(db: Session = Depends(get_db),
                  page: int =0, size: int = 10, keyword = ''):
    total, _user_list = user_crud.get_user_list(
        db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'user_list': _user_list
    }
#직접작성
@router.get("/detail/{username}", response_model=user_schema.User)
def user_detail(username: str, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, username=username)
    return user

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)    # 파라미터로 받은 값을갖는 유저 등록 여부 확인
    if user:            # null이 아니라면
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        # pwd_context.verify 암호화 되지 않은 비밀번호를 암호화하여 데이터베이스에 저장된 암호와 일치하는지 판단한다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "authority": user.authority
    }

# 헤더 정보의 토큰값으로 사용자 정보를 조회
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user

#직접작성
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(_user_delete: user_schema.UserDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user = user_crud.get_user(db, username=_user_delete.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.username != db_user.uername and current_user.authority is False:                # 관리자 권한이면 가능
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    user_crud.delete_user(db=db, db_user=db_user)

#직접 작성
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def user_update(_user_update: user_schema.UserUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user = user_crud.get_user(db, username=_user_update.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_user.id and current_user.authority is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,        # 본인 계정만 수정 가능
                            detail="수정 권한이 없습니다.")
    # 비밀번호 일치여부 확인
    '''
    if  not pwd_context.verify(form_data.password, db_user.password):
        # pwd_context.verify 암호화 되지 않은 비밀번호를 암호화하여 데이터베이스에 저장된 암호와 일치하는지 판단한다.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    '''
    user_crud.update_user(db=db, db_user=db_user,
                                  user_update=_user_update)