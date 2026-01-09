# ALB 생성
resource "aws_lb" "king_alb" {
  name               = "king-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.terraform_sg_alb.id]
  subnets            = [aws_subnet.PUB_subnet_2A.id, aws_subnet.PUB_subnet_2C.id] # 퍼블릭 서브넷 사용

  tags = { Name = "king-alb" }
}

# 대상 그룹(Target Group) - 나중에 EKS 서비스와 연결될 곳
resource "aws_lb_target_group" "tg" {
  name     = "king-alb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.king_vpc.id

  health_check {
    path     = "/"
    matcher  = "200"
    interval = 30
    timeout  = 5
  }
}

# 리스너 (HTTP -> HTTPS 리다이렉트 설정도 가능하지만 우선 80 오픈)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.king_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

# 리스너 (HTTPS 443 추가 - 인증서 연결)
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.king_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }

  # 📍 수정 포인트: cert_validation 대신 cert_valid (위에서 추가한 것)를 기다리게 합니다.
  depends_on = [aws_acm_certificate_validation.cert_valid]
}
