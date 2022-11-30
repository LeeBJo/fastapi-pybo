from datetime import datetime

from testModel import HealthInfo, User, Answer
from domain.health_info.health_info_schema import HealthInfoCreate
from sqlalchemy.orm import Session


def get_health_info_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''): #skip:조회데이터의 시작위치, limit:시작위치로부터 가져올 데이터 건수
    health_info_list = db.query(HealthInfo)
    if keyword:
        search = '%%{}%%'.format(keyword)
        health_info_list = health_info_list \
            .filter(HealthInfo.subject.ilike(search) |  # 정보 제목
                    HealthInfo.content.ilike(search) |  # 정보 내용
                    HealthInfo.link.ilike(search)       # 정보 링크
                    )
    total = health_info_list.count()
    health_info_list = health_info_list.order_by(HealthInfo.create_date.desc()) \
        .offset(skip).limit(limit).all()
    return total, health_info_list             # (전체 건수, 페이징 적용된 질문 목록)

def create_health_info(db: Session, health_info_create: HealthInfoCreate):
    db_health_info = HealthInfo(subject=health_info_create.subject,
                           content=health_info_create.content,
                           link=health_info_create.link,
                           create_date=datetime.now())
    db.add(db_health_info)
    db.commit()

def get_health_info(db: Session, health_info_id: int):
    health_info = db.query(HealthInfo).get(health_info_id)
    return health_info

def delete_health_info(db: Session, db_health_info: HealthInfo):
    db.delete(db_health_info)
    db.commit()