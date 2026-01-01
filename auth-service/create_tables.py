# create_tables.py

# 현재 디렉토리의 database.py와 models.py를 임포트
import database
import models

# Base.metadata를 사용하여 테이블 생성
print("Attempting to create tables...")
database.Base.metadata.create_all(bind=database.engine)
print("Tables created successfully!")

