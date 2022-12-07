from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from testdb import get_db
from domain.recommend_diet_question import r_question_schema, r_question_crud
from domain.user.user_router import get_current_user
from testModel import User

router = APIRouter(
    prefix="/api/rquestion",
)


@router.get("/list", response_model=r_question_schema.RQuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword: str = '', is_admin: bool = False, username: str = ''):
    total, _question_list = r_question_crud.get_question_list(
        db, skip=page * size, limit=size, keyword=keyword, is_admin=is_admin, username=username)
    return {
        'total': total,
        'question_list': _question_list
    }


@router.get("/detail/{question_id}", response_model=r_question_schema.RQuestion)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = r_question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: r_question_schema.RQuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    r_question_crud.create_question(db=db, question_create=_question_create,
                                  user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: r_question_schema.RQuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = r_question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    r_question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: r_question_schema.RQuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = r_question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    r_question_crud.delete_question(db=db, db_question=db_question)