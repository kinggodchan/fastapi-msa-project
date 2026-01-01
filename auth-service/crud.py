# crud.py

from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext
from typing import Union

# 비밀번호 해싱을 위한 CryptContext 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 헬퍼 함수: 비밀번호 해시 생성
def get_password_hash(password):
    return pwd_context.hash(password)

# 1. 특정 사용자 이름으로 사용자 찾기 (Read)
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# 2. 새 사용자 생성 (Create)
def create_user(db: Session, user: schemas.UserCreate):
    # 비밀번호 해시 생성
    hashed_password = get_password_hash(user.password)

    # DB 모델 인스턴스 생성 및 저장
    db_user = models.User(username=user.username, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 헬퍼 함수: 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """일반 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 반환합니다."""
    # .verify() 메서드가 해시된 문자열과 비교를 처리합니다.
    return pwd_context.verify(plain_password, hashed_password)

# 헬퍼 함수: 사용자 인증 (로그인 시 사용)
def authenticate_user(db: Session, username: str, password: str) -> Union[models.User, None]:
    """사용자 이름으로 사용자를 찾고, 비밀번호를 검증합니다."""
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    # .dict() 대신 .model_dump()를 사용하여 딕셔너리로 변환합니다.
    # 만약 model_dump()가 없는 구버전이라면 다시 .dict()로 시도하세요.
    try:
        db_post = models.Post(**post.model_dump(), owner_id=user_id)
    except AttributeError:
        db_post = models.Post(**post.dict(), owner_id=user_id)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

