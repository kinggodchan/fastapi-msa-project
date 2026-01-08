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
        # 🚀 수정 핵심:
        # 1. region_name을 명시
        # 2. endpoint_url을 https://s3.ap-northeast-2.amazonaws.com 로 고정
        # 3. addressing_style을 path로 유지

        region = "ap-northeast-2"
        s3_config = Config(
            region_name=region,
            signature_version='s3v4',
            s3={'addressing_style': 'path'},
            connect_timeout=10,
            read_timeout=10
        )

        s3 = boto3.client(
            's3',
            config=s3_config,
            endpoint_url=f"https://s3.{region}.amazonaws.com" # 다시 명시해봅니다.
        )

        print(f"🚀 Attempting to connect to S3 Bucket: {settings.BUCKET_NAME}", flush=True)

        # settings에서 가져온 key 값 확인
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.MODEL_S3_KEY)

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
