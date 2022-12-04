from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from testdb import get_db
from domain.recommend_diet_answer import r_answer_schema, r_answer_crud
from domain.recommend_diet_question import r_question_crud
from domain.user.user_router import get_current_user
from testModel import User

router = APIRouter(
    prefix="/api/ranswer",
)


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                  _answer_create: r_answer_schema.RAnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # create answer
    question = r_question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    r_answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user=current_user)


@router.get("/detail/{answer_id}", response_model=r_answer_schema.RAnswer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = r_answer_crud.get_answer(db, answer_id=answer_id)
    return answer


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: r_answer_schema.RAnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = r_answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    r_answer_crud.update_answer(db=db, db_answer=db_answer,
                              answer_update=_answer_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: r_answer_schema.RAnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = r_answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    r_answer_crud.delete_answer(db=db, db_answer=db_answer)