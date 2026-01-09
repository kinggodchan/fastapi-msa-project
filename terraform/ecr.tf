resource "aws_ecr_repository" "terraform_ecr" { # 하이픈(-)을 언더바(_)로 수정
  name                 = "terraform-ecr"        # 실제 ECR 이름은 하이픈 유지 가능
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  tags = {
    Name = "terraform-ecr"
  }
}
