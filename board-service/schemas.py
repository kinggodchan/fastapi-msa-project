# schemas.py

from pydantic import BaseModel
from typing import Union

# 1. 회원가입 요청 시 사용할 입력 스키마 (클라이언트 -> 서버)
class UserCreate(BaseModel):
    username: str
    password: str

# 2. DB에서 읽어온 사용자 정보를 클라이언트에게 반환할 출력 스키마 (서버 -> 클라이언트)
class User(BaseModel):
    id: int
    username: str
    is_active: bool

    # SQLAlchemy 모델과 Pydantic 모델을 호환시키기 위한 설정
    class Config:
        orm_mode = True

# 3. 사용자 로그인 요청 시 사용할 입력 스키마
class UserLogin(BaseModel):
    username: str
    password: str

# 4. 로그인 성공 시 반환할 토큰 스키마
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 5. 토큰에 저장될 데이터 스키마 (선택 사항이지만 안전을 위해 정의)
class TokenData(BaseModel):
    username: Union[str, None] = None

# 6. 게시판 작성 시 사용할 입력 스키마
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

