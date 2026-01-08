from fastapi import FastAPI, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Union, Any
from datetime import timedelta
import crud
import models
import schemas
import database
import auth
from fastapi.security import OAuth2PasswordRequestForm

# --- [수정] ML 관련 라이브러리 및 로딩 로직 제거됨 ---

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 기본 API 경로
@app.get("/")
def read_root():
    return {"Hello": "World from FastAPI Auth Service"}

# --- [수정] /predict 엔드포인트는 이제 iris-serving-service에서 담당하므로 삭제 ---

@app.get("/api/v1/status")
def api_status():
    return {"status": "ok", "service": "Auth API", "db_connected": True}

# 로그인 엔드포인트: JWT 토큰 발급
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 사용자 정보 조회 (보호된 엔드포인트)
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# 사용자 등록
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# 게시판 관련 기능
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)
