from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from domain.health_info import health_info_router
from domain.recommend_diet_answer import r_answer_router
from domain.recommend_diet_question import r_question_router

from testdb import SessionLocal
from testModel import User, HealthInfo, Question
import random

import smtplib
from email.mime.text import MIMEText
import threading
import time
import datetime

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(health_info_router.router)
app.include_router(r_answer_router.router)
app.include_router(r_question_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")


def send_Hinfo(email: str):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    db = SessionLocal()

    s.starttls()
    s.login('tnghwk0661@gmail.com', 'tolvphsgeoykzivr')

    data = random.choice(db.query(HealthInfo).all())

    msg = MIMEText(data.content)
    msg['Subject'] = '[건강 정보] '+data.subject #'제목 : 메일 보내기 테스트입니다.'

    s.sendmail("tnghwk0661@gmail.com", email, msg.as_string())
    s.quit()


def send_hot(email: str):
    hit = 3
    s = smtplib.SMTP('smtp.gmail.com', 587)
    db = SessionLocal()

    s.starttls()
    s.login('tnghwk0661@gmail.com', 'tolvphsgeoykzivr')
    datas = db.query(Question).all()
    data = []
    for i in range(len(datas)):
        if len(datas[i].voter) >= hit:
            data.append(datas[i])
    t = random.choice(data)
    msg = MIMEText(t.content)
    msg['Subject'] = '[인기 게시물] '+t.subject

    s.sendmail("tnghwk0661@gmail.com", email, msg.as_string())
    s.quit()

def pickup():
    db = SessionLocal()
    while True:
        now_time = datetime.datetime.now()
        if now_time.hour == 18 and now_time.minute == 22:
            h = db.query(User).filter(User.alarmAccepted==True).all() # db 조회
            for i in h:
                send_Hinfo(i.email)
                send_hot(i.email)
            time.sleep(datetime.timedelta(days=1).total_seconds())



t = threading.Thread(target=pickup,)
t.start()


# 모델링 -> 도메인생성 -> 스키마 -> crud -> 라우터 -> 메인등록
# 모델 수정/추가 -> db update (alembic) -> 스키마 -> crud -> 라우터 -> 메인등록
# 연산 추가 : 스키마에 연산 추가 -> crud -> 라우터
# DB 연산
# 라우팅이란 FastAPI가 요청받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위를 말한다.