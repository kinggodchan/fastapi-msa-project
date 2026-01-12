# 1. Application Load Balancer
resource "aws_lb" "alb" {
  name               = "terraform-king-alb" # 직접 이름 지정
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.terraform_sg_alb.id]

  # ✅ 직접 서브넷 참조 (03-subnet.tf에서 정의한 이름 사용)
  subnets = [aws_subnet.PUB_subnet_2A.id, aws_subnet.PUB_subnet_2C.id]

  tags = {
    Name = "terraform-king-alb"
  }
}

# 2. Target Group
resource "aws_lb_target_group" "tg" {
  name     = "terraform-king-tg"
  port     = 80
  protocol = "HTTP"

  # ✅ 직접 VPC 참조 (02-vpc.tf에서 정의한 이름 사용)
  vpc_id = aws_vpc.king_vpc.id

  health_check {
    path                = "/health"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# 3. HTTP 리스너 (Redirect to HTTPS)
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# 4. HTTPS 리스너
resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}
