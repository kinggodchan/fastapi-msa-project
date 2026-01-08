import os

class Config:
    # 1. 실제 모델이 들어있는 버킷 이름으로 수정
    BUCKET_NAME = "sagemaker-ap-northeast-2-266735812372"
    
    # 2. 찾으신 'S3 모델 아티팩트'의 경로 부분을 그대로 입력
    MODEL_S3_KEY = "pipelines-9x6ooi9s2j3p-IrisTrain-3xPsVBJdtW/output/model.tar.gz"
    
    # 3. 리전 확인
    AWS_REGION = "ap-northeast-2"

settings = Config()
