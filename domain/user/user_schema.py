from pydantic import BaseModel, validator, EmailStr
import datetime


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    alarmAccepted: bool
    authority: bool
    modify_date: datetime.datetime | None = None  # 수정일

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class User(BaseModel):
    id: int
    username: str
    email: str
    alarmAccepted: bool
    authority: bool

    class Config:               # user 모델의 항목들이 자동으로 user schema로 매핑
        orm_mode = True

class UserList(BaseModel):
    total: int = 0
    user_list: list[User] = []

class UserUpdate(UserCreate):       # UserCreate class 상속
    newpwd: str

class UserDelete(BaseModel):
    username: str                #username으로 교체 고려


class Token(BaseModel):     # 로그인 출력항목
    access_token: str
    token_type: str
    username: str
    authority: bool