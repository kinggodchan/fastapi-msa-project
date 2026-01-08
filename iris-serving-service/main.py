import io
import tarfile
import joblib
import boto3
import pandas as pd
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from config import settings
# 1. 추가: S3 접속 설정을 위한 Config 임포트
from botocore.config import Config

app = FastAPI(title="Iris ML Serving Service")

model = None

def load_model_from_s3():
    global model
    try:
        # 2. 수정: S3 접속 방식 보강 (경로 기반 호출 및 리전 고정)
        s3_config = Config(
            region_name=settings.AWS_REGION,
            signature_version='s3v4',
            s3={'addressing_style': 'path'}  # 주소 오류(Endpoint URL) 해결을 위한 핵심 설정
        )

        # 3. 수정: 설정을 포함하여 클라이언트 생성
        s3 = boto3.client('s3', config=s3_config)

        print(f"🚀 Attempting to connect to S3 Bucket: {settings.BUCKET_NAME}")
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.MODEL_S3_KEY)

        # 기존 로직: 메모리에서 바로 압축 해제 및 로드
        with tarfile.open(fileobj=io.BytesIO(response['Body'].read()), mode="r:gz") as tar:
            # SageMaker에서 만든 model.joblib을 메모리에서 바로 로드
            content = tar.extractfile("model.joblib")
            model = joblib.load(io.BytesIO(content.read()))
            
        print("✅ SageMaker ML Model loaded successfully from S3")
        
    except Exception as e:
        # 에러 발생 시 상세 정보 출력
        print(f"❌ Model load failed: {str(e)}")

@app.on_event("startup")
async def startup():
    load_model_from_s3()

@app.get("/health")
def health():
    return {"status": "up", "service": "iris-serving"}

@app.post("/predict")
async def predict(data: List[List[float]]):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    # 입력 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return {"result": prediction.tolist()}
