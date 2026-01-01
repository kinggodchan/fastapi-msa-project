# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from base_class import Base # base_class.py

import models # 모델 클래스를 로드하여 Base.metadata에 등록

# 1. DB 연결 엔진 생성
engine = create_engine(
    DATABASE_URL
)

# 2. DB 세션 생성기 정의
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. DB 테이블 생성 함수 (유틸리티)
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# -----------------------------------------------------
# 추가: DB 세션을 제공하는 의존성 함수 (get_db를 이곳으로 이동)
# -----------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------------
# 추가: DB 테이블 생성 함수 (이전에 사용했던 함수)
# -----------------------------------------------------
def create_db_tables():
    from . import models # models 모듈을 임포트해야 테이블 구조를 알 수 있습니다.
    Base.metadata.create_all(bind=engine)

