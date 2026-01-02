# auth-service/config.py
import os

# 1. 환경 변수에서 값을 읽어옵니다. (값이 없으면 기본값 사용)
DB_USER = os.getenv("DB_USER", "test01")
DB_PASSWORD = os.getenv("DB_PASSWORD", "P@ssw0rd")
DB_HOST = os.getenv("DB_HOST", "mysql")  # 쿠버네티스 서비스 이름인 'mysql'을 사용
DB_NAME = os.getenv("DB_NAME", "fastapi_db")


# 수정된 DATABASE_URL
DATABASE_URL = f"mysql+pymysql://test01:P%40ssw0rd@{DB_HOST}:3306/fastapi_db"
