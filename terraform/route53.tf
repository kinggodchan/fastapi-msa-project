# 1. Route 53 호스팅 영역 생성
resource "aws_route53_zone" "main" {
  name = "a4rism.shop"

  tags = {
    Name = "a4rism-shop-zone"
  }
}

# 2. 가비아에 입력할 네임서버 주소 확인용 Output
# terraform apply 후에 화면에 출력됩니다.
output "route53_nameservers" {
  value       = aws_route53_zone.main.name_servers
  description = "가비아 네임서버 설정에 입력해야 할 4개의 주소입니다."
}
