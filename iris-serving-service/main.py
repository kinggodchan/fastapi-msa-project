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
        # 1. 설정을 최소화하여 VPC 엔드포인트가 자동으로 작동하게 합니다.
        s3_config = Config(
            region_name=settings.AWS_REGION,
            signature_version='s3v4',
            connect_timeout=5,
            read_timeout=5
        )

        # 🚀 수정 포인트: endpoint_url을 삭제하여 AWS 내부망을 타게 합니다.
        s3 = boto3.client('s3', config=s3_config)

        # flush=True를 넣어 로그가 즉시 찍히게 합니다.
        print(f"🚀 Attempting to connect to S3 Bucket: {settings.BUCKET_NAME}", flush=True)
        
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.MODEL_S3_KEY)

        with tarfile.open(fileobj=io.BytesIO(response['Body'].read()), mode="r:gz") as tar:
            content = tar.extractfile("model.joblib")
            model = joblib.load(io.BytesIO(content.read()))

        print("✅ SageMaker ML Model loaded successfully from S3", flush=True)

    except Exception as e:
        # 에러 종류를 파악하기 위해 type(e)를 추가합니다.
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
        # 모델이 안 로드되었을 때의 상태를 명확히 반환
        raise HTTPException(status_code=503, detail="Model is not loaded yet")

    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return {"result": prediction.tolist()}
