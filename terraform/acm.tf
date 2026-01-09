# 인증서 신청
resource "aws_acm_certificate" "cert" {
  domain_name               = "*.a4rism.shop"
  validation_method         = "DNS"
  subject_alternative_names = ["a4rism.shop"]

  tags = { Name = "a4rism-cert" }

  lifecycle {
    create_before_destroy = true
  }
}

# DNS 검증 레코드 생성
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.main.zone_id
}

# 23-acm.tf 파일 맨 아래에 추가하세요
resource "aws_acm_certificate_validation" "cert_valid" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
