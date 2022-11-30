from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from testdb import get_db
from domain.question import question_schema, question_crud
from domain.health_info import health_info_crud, health_info_schema
from domain.user.user_router import get_current_user
from testModel import User


router = APIRouter(
    prefix="/api/health_info",
)

@router.get("/list", response_model=health_info_schema.HealthInfoList)   # 리턴타입 = health_schema의 HealthInfoList
def health_info_list(db: Session = Depends(get_db),
                  page: int =0, size: int = 10, keyword = ''):
    total, _health_info_list = health_info_crud.get_health_info_list(
        db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'health_info_list': _health_info_list
    }

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def health_info_create(_health_info_create: health_info_schema.HealthIfoCreate,
                    db: Session = Depends(get_db)):
    health_info_crud.create_health_info(db=db, health_info_create=_health_info_create)

@router.get("/detail/{health_info_id}", response_model=health_info_schema.HealthInfo)
def health_info_detail(health_info_id: int, db: Session = Depends(get_db)):
    health_info = health_info_crud.get_health_info(db, health_info_id=health_info_id)
    return health_info

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def health_info_delete(_health_info_delete: health_info_schema.HealthInfoDelete,
                    db: Session = Depends(get_db)):
    db_health_info = health_info_crud.get_health_info(db, health_info_id=_health_info_delete.health_info_id)
    if not db_health_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    health_info_crud.delete_health_info(db=db, db_health_info=db_health_info)