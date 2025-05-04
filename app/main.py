from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "baseball.db")

app = FastAPI()

# 요청 바디 형식
class Question(BaseModel):
    question_type: str  # "player", "team", "term"
    keyword: str         # 예: "전준우", "롯데", "타율"

DB_PATH = "./database/baseball.db"

# DB 조회 함수
def search_database(q_type, keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if q_type == "player":
        cursor.execute("SELECT name, team, position, stats FROM players WHERE name = ?", (keyword,))
        row = cursor.fetchone()
        if row:
            return f"{row[0]} 선수는 {row[1]} 팀 소속의 {row[2]}입니다. 주요 성적: {row[3]}"
        else:
            return "해당 선수 정보를 찾을 수 없습니다."

    elif q_type == "team":
        cursor.execute("SELECT team_name, wins, losses, draws, win_rate, rank FROM teams WHERE team_name = ?", (keyword,))
        row = cursor.fetchone()
        if row:
            return f"{row[0]} 팀은 {row[1]}승 {row[2]}패 {row[3]}무, 승률 {row[4]}, 현재 순위 {row[5]}위입니다."
        else:
            return "해당 팀 정보를 찾을 수 없습니다."

    elif q_type == "term":
        cursor.execute("SELECT term, description FROM terms WHERE term = ?", (keyword,))
        row = cursor.fetchone()
        if row:
            return f"{row[0]}: {row[1]}"
        else:
            return "해당 용어 정보를 찾을 수 없습니다."

    else:
        return "지원하지 않는 질문 유형입니다."

# FastAPI 엔드포인트
@app.post("/query")
def get_answer(q: Question):
    result = search_database(q.question_type, q.keyword)
    return {"answer": result}