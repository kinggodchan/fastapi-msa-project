import io
import tarfile
import joblib
import boto3
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from config import settings

app = FastAPI(title="Iris ML Serving Service")

model = None

def load_model_from_s3():
    global model
    try:
        s3 = boto3.client('s3', region_name=settings.AWS_REGION)
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.MODEL_S3_KEY)
        
        with tarfile.open(fileobj=io.BytesIO(response['Body'].read()), mode="r:gz") as tar:
            # SageMaker에서 만든 model.joblib을 메모리에서 바로 로드
            content = tar.extractfile("model.joblib")
            model = joblib.load(io.BytesIO(content.read()))
        print("✅ SageMaker ML Model loaded successfully from S3")
    except Exception as e:
        print(f"❌ Model load failed: {e}")

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
    
    # 입력 데이터를 데이터프레임으로 변환 (Feature names 무시 버전)
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return {"result": prediction.tolist()}
