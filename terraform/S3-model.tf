# AI 모델 저장용 S3 버킷 생성
resource "aws_s3_bucket" "model_bucket" {
  bucket        = "kinggodchan-model-bucket"
  force_destroy = true # 연습용이므로 삭제 시 내부 파일 포함 강제 삭제

  tags = {
    Name = "kinggodchan-model-bucket"
  }
}
