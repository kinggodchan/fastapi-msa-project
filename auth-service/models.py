
# models.py 상단 수정
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text # <-- 이 부분에 ForeignKey와 Text를 꼭 추가해야 합니다!
from base_class import Base

# User 테이블 구조 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

# Post 테이블 구조 정의
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text) # 상단에 Text를 import 했으므로 이제 인식됩니다.
    owner_id = Column(Integer, ForeignKey("users.id")) # 상단에 ForeignKey를 import 했으므로 이제 인식됩니다.

