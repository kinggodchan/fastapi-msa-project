import io
import tarfile
import joblib
import boto3
import pandas as pd
import os
from fastapi import FastAPI, HTTPException
from typing import List
from config import settings
from botocore.config import Config

app = FastAPI(title="Iris ML Serving Service")

model = None

def load_model_from_s3():
    global model
    try:
        # 🚀 수정 핵심: addressing_style을 'path'로 설정하여 점(.)이 포함된 버킷 문제를 해결합니다.
        s3_config = Config(
            region_name=settings.AWS_REGION,
            signature_version='s3v4',
            s3={'addressing_style': 'path'}, 
            connect_timeout=10,
            read_timeout=10
        )

        # endpoint_url 없이 기본 클라이언트를 생성하여 VPC 엔드포인트를 타게 합니다.
        s3 = boto3.client('s3', config=s3_config)

        print(f"🚀 Attempting to connect to S3 Bucket: {settings.BUCKET_NAME}", flush=True)

        # Key 값의 시작 부분에 혹시 모를 '/' 제거
        model_key = settings.MODEL_S3_KEY.lstrip('/')
        
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=model_key)

        with tarfile.open(fileobj=io.BytesIO(response['Body'].read()), mode="r:gz") as tar:
            content = tar.extractfile("model.joblib")
            model = joblib.load(io.BytesIO(content.read()))

        print("✅ SageMaker ML Model loaded successfully from S3", flush=True)

    except Exception as e:
        print(f"❌ Model load failed: {type(e).__name__} - {str(e)}", flush=True)

@app.on_event("startup")
async def startup():
    print("🔔 Application is starting up...", flush=True)
    load_model_from_s3()

@app.get("/health")
def health():
    return {"status": "up", "model_loaded": model is not None}

@app.post("/predict")
async def predict(data: List[List[float]]):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded yet")

    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return {"result": prediction.tolist()}
