from pydantic import BaseModel, validator   # validator : 빈칸 입력 방지
import datetime

class HealthInfo(BaseModel):

    id: int
    subject: str
    content: str
    link: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

class HealthInfoList(BaseModel):
    total: int = 0
    health_info_list: list[HealthInfo] = []

class HealthInfoCreate(BaseModel):
    subject: str
    content: str
    link: str

    @validator('subject', 'content', 'link')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class HealthInfoDelete(BaseModel):
    health_info_id:int