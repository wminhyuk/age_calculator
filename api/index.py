from fastapi import FastAPI
from datetime import datetime, date
from typing import Dict
import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")
@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.get("/api/py/ageCalculator/{birthday}")
def age_calculator(birthday: str) -> Dict[str, str]:
    """
    생년월일을 입력받아 만나이를 계산하는 API
    :param birthday: 생년월일 (형식: YYYY-MM-DD)
    :return: 생년월일 및 만나이를 포함한 JSON 응답
    """
    today = date.today()
    birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    age = today.year - birth_date.year

    # 생일 반영 코드
    if (birth_date.month > today.month) or (birth_date.month == today.month and birth_date.day > today.day):
        age -= 1

    # 띠 리스트
    zodiac_animals = [
    "🐀 Rat",      # 자 - 쥐
    "🐂 Ox",       # 축 - 소
    "🐅 Tiger",    # 인 - 호랑이
    "🐇 Rabbit",   # 묘 - 토끼
    "🐉 Dragon",   # 진 - 용
    "🐍 Snake",    # 사 - 뱀
    "🐎 Horse",    # 오 - 말
    "🐐 Goat",     # 미 - 양
    "🐒 Monkey",   # 신 - 원숭이
    "🐓 Rooster",  # 유 - 닭
    "🐕 Dog",      # 술 - 개
    "🐖 Pig"       # 해 - 돼지
    ]
    zodiac = zodiac_animals[(birth_date.year-4) % 12]


    return {
            "birthday": birthday,
            "age": str(age),
            "basedate": str(today),
            "zodiac": zodiac,
            "message": "Age calculated successfully!",
            "os-name": "PRETTY_NAME"
            }

def get_os_pretty_name():
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('PRETTY_NAME='):
                return line.split('=')[1].replace('\n', '').strip('"')
    return None

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": os.getenv("DB_NAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

@app.get("/api/py/select_all")
def select_all():
    query = """
    SELECT
        l.menu_name,
        m.name,
        l.dt
    FROM
        lunch_menu l
        inner join member m
        on l.member_id = m.id
    """
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        cur = conn.execute(query)
        rows = cur.fetchall()
        return rows
