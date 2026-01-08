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
from botocore.config import Config

app = FastAPI(title="Iris ML Serving Service")

model = None

def load_model_from_s3():
    global model
    try:
        s3_config = Config(
            region_name=settings.AWS_REGION,
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        )

        # 🚀 수정 포인트: endpoint_url을 직접 명시하여 연결 경로를 강제합니다.
        s3 = boto3.client(
            's3', 
            config=s3_config,
            endpoint_url=f"https://s3.{settings.AWS_REGION}.amazonaws.com"
        )

        print(f"🚀 Attempting to connect to S3 Bucket: {settings.BUCKET_NAME}")
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.MODEL_S3_KEY)

        with tarfile.open(fileobj=io.BytesIO(response['Body'].read()), mode="r:gz") as tar:
            content = tar.extractfile("model.joblib")
            model = joblib.load(io.BytesIO(content.read()))

        print("✅ SageMaker ML Model loaded successfully from S3")

    except Exception as e:
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

    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return {"result": prediction.tolist()}
