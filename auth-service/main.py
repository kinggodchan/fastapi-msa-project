# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union, Any
from datetime import timedelta
import crud
import models
import schemas
import database
import auth
from fastapi.security import OAuth2PasswordRequestForm
#from database import SessionLocal, engine, get_db

# --- [ML 추가] 모델 로드용 라이브러리 ---
import joblib
import os
import numpy as np
# ------------------------------------


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- [ML 추가] 모델 경로 및 전역 변수 설정 ---
MODEL_PATH = "/app/my_actual_model.pkl"
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"✅ 모델 로드 성공: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ 모델 로드 중 오류 발생: {e}")
    else:
        print(f"⚠️ 모델 파일을 찾을 수 없습니다: {MODEL_PATH}")
# --------------

# 기본 API 경로
@app.get("/")
def read_root():
    return {"Hello": "World from FastAPI"}

# --- [ML 추가] 예측(Prediction) 엔드포인트 ---
app.post("/predict")
def predict(payload: Any):  # Any를 사용하여 우선 데이터를 모두 받습니다.
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # 1. 데이터 추출 로직
        # payload가 {'data': [...]} 형태인 경우
        if isinstance(payload, dict) and "data" in payload:
            actual_data = payload["data"]
        # payload가 바로 리스트 [...] 인 경우
        elif isinstance(payload, list):
            actual_data = payload
        else:
            actual_data = payload

        # 2. 넘파이 배열 변환 및 예측
        input_data = np.array(actual_data).reshape(1, -1)
        prediction = model.predict(input_data)
        
        return {
            "status": "success",
            "input": actual_data,
            "prediction": prediction.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# --------------------------------------------

@app.get("/api/v1/status")
def api_status():
    return {"status": "ok", "service": "Backend API", "db_connected": True}

# 새로운 회원가입 엔드포인트
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. 사용자 이름 중복 확인
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # 2. 사용자 생성 및 DB 저장 (crud.py 호출)
    return crud.create_user(db=db, user=user)

# -----------------------------------------------------
# 1. 로그인 엔드포인트: JWT 토큰 발급
# -----------------------------------------------------
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # OAuth2PasswordRequestForm 사용
    db: Session = Depends(database.get_db)
):
    # 1. 사용자 인증 시도 (crud.py에서 만든 함수 사용)
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        # 인증 실패 시 401 UNAUTHORIZED 예외 발생
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. 인증 성공 시 액세스 토큰 생성
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, # 토큰에 저장할 데이터 (사용자 이름)
        expires_delta=access_token_expires
    )

    # 3. 생성된 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}


# -----------------------------------------------------
# 2. 보호된 엔드포인트: 현재 로그인 사용자 정보 조회
# -----------------------------------------------------
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)): # auth.get_current_user 사용
    """토큰을 제공한 사용자의 정보를 반환합니다."""
    return current_user


# -----------------------------------------------------
# 3. (기존) 사용자 등록 엔드포인트 유지
# -----------------------------------------------------
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# 4. 게시판 작성
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

