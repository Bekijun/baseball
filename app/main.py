from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
import json
import re
from konlpy.tag import Okt

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "baseball.db")

app = FastAPI()
okt = Okt()

# 요청 모델
class Question(BaseModel):
    question_type: str
    keyword: str

class NLQuery(BaseModel):
    text: str

# 컬럼 값 리스트 추출
def get_all_values_from_column(table, column):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column} FROM {table}")
    return [row[0] for row in cursor.fetchall()]

# 자연어 분석: 명사 + 대문자 약어 인식
def extract_terms(text):
    okt_nouns = okt.nouns(text)
    regex_terms = re.findall(r"[A-Z]{2,}", text)  # <- 수정된 정규표현식
    print("🧠 OKT 명사:", okt_nouns)
    print("🔡 정규표현식 대문자:", regex_terms)
    return list(set(okt_nouns + regex_terms))

# 분석 함수
def analyze_question(text):
    nouns = extract_terms(text)

    players = get_all_values_from_column("players", "name")
    teams = get_all_values_from_column("teams", "team_name")
    terms = get_all_values_from_column("terms", "term")
    extra_fields = ["타율", "홈런", "출루율", "타점", "삼진", "볼넷", "안타", "키", "몸무게", "OPS", "ERA"]

    q_type = ""
    keyword = ""
    field = ""

    for n in nouns:
        if n in players:
            q_type = "player"
            keyword = n
        elif n in teams:
            q_type = "team"
            keyword = n
        elif n in terms or n in extra_fields:
            field = n
            if not q_type:
                q_type = "term"

    if not keyword and field:
        keyword = field

    return {
        "question_type": q_type,
        "keyword": keyword,
        "field": field
    }

# DB 검색 함수
def search_database(q_type, keyword, field=None, season='2024'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if q_type == "player":
        cursor.execute("SELECT id, name, team, position, introduction, height, weight FROM players WHERE name = ?", (keyword,))
        row = cursor.fetchone()
        if not row:
            return "해당 선수 정보를 찾을 수 없습니다."

        player_id = row[0]
        name = row[1]

        if field in ["타율", "홈런", "출루율", "타점", "삼진", "볼넷", "안타"]:
            cursor.execute(
                "SELECT value FROM player_stats WHERE player_id = ? AND stat_type = ? AND season = ?",
                (player_id, field, season)
            )
            stat_row = cursor.fetchone()
            if stat_row:
                return f"{name}의 {season}년 {field}은 {stat_row[0]}입니다."
            else:
                return f"{name} 선수의 {field} 정보를 찾을 수 없습니다."

        elif field == "키":
            return f"{name}의 키는 {row[5]}cm입니다."
        elif field == "몸무게":
            return f"{name}의 몸무게는 {row[6]}kg입니다."
        else:
            return f"{name} 선수는 {row[2]} 팀 소속의 {row[3]}입니다.\n소개: {row[4]}"

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

    return "지원하지 않는 질문 유형입니다."

# 명시적 쿼리
@app.post("/query")
def get_answer(q: Question):
    result = search_database(q.question_type, q.keyword)
    return {"answer": result}

# 자연어 쿼리
@app.post("/nl_query")
def handle_nl_query(q: NLQuery):
    parsed = analyze_question(q.text)

    if not parsed.get("keyword") and parsed.get("field"):
        parsed["keyword"] = parsed["field"]

    if not parsed.get("question_type") or not parsed.get("keyword"):
        return {"answer": "질문을 이해하지 못했습니다."}

    result = search_database(
        parsed["question_type"],
        parsed["keyword"],
        field=parsed.get("field")
    )
    return {"answer": result}

    print("🧪 분석 결과:", parsed)
