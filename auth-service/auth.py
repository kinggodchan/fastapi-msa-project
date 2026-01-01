# auth.py

from datetime import datetime, timedelta, timezone
from typing import Any, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import schemas
import crud
import database

# -----------------------------------------------------
# 1. 환경 설정 (실제 프로젝트에서는 환경 변수로 관리해야 합니다)
# -----------------------------------------------------
# 비밀 키: 토큰 서명에 사용되는 비밀 키입니다. 강력하고 긴 문자열을 사용해야 합니다.
SECRET_KEY = "your-very-secret-key-replace-me-soon"
ALGORITHM = "HS256" # JWT 서명 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 토큰 만료 시간 (분 단위)

# OAuth2 스키마 정의: /token 엔드포인트에서 토큰을 요청하도록 지정합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -----------------------------------------------------
# 2. JWT 토큰 생성 및 검증 함수
# -----------------------------------------------------

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """주어진 데이터를 이용해 JWT 액세스 토큰을 생성합니다."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 만료 시간이 지정되지 않으면 기본 만료 시간 사용
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # 'exp' (만료 시간) 클레임 추가
    to_encode.update({"exp": expire})

    # JWT 토큰 생성
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """JWT 토큰을 검증하고, 토큰 데이터를 반환합니다."""
    try:
        # 토큰 디코딩 (검증 포함)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 'sub' (주제) 클레임에서 사용자 이름 추출
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # 토큰 데이터를 Pydantic 모델로 변환 (데이터 검증)
        token_data = schemas.TokenData(username=username)

    except JWTError:
        # 토큰 디코딩 중 오류 발생 (유효하지 않은 서명, 만료 등)
        raise credentials_exception

    return token_data

# -----------------------------------------------------
# 3. 의존성 주입 함수 (Dependency)
# -----------------------------------------------------

# 토큰 인증에 실패했을 때 사용할 예외 정의
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    현재 로그인한 사용자 객체를 반환합니다.
    이 함수는 보호된 API 엔드포인트의 Depends() 인자로 사용됩니다.
    """
    # 1. 토큰 검증 및 사용자 이름 추출
    token_data = verify_access_token(token, CREDENTIALS_EXCEPTION)

    # 2. 데이터베이스에서 사용자 찾기
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user

