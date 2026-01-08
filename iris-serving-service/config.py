import os

class Config:
    # SageMaker 결과물 경로 (아까 성공한 주소)
    BUCKET_NAME = "amazon-sagemaker-266735812372-ap-northeast-2-9d73180cc111"
    MODEL_S3_KEY = "dzd-co6rwit4e5zqvs/bnqjlbw91x4is8/dev/data/model_final.tar.gz"
    AWS_REGION = "ap-northeast-2"

settings = Config()
