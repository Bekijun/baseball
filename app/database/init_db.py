import sqlite3

# SQLite DB 연결 및 초기화
conn = sqlite3.connect("baseball.db")
cursor = conn.cursor()

# SQL 파일 실행
with open("baseball_schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

print("✅ baseball.db 파일이 생성되었습니다.")

conn.commit()
conn.close()