# 1. Bastion 서버용 보안 그룹
resource "aws_security_group" "terraform_sg_bastion" { # 하이픈(-)을 언더바(_)로 수정
  name        = "terraform-sg-bastion"
  description = "for Bastion Server"
  vpc_id      = aws_vpc.king_vpc.id

  tags = {
    Name = "terraform-sg-bastion"
  }

  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for ping"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for SSH"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for HTTP"
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for DB access from outside"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. RDS 전용 보안 그룹
resource "aws_security_group" "terraform_sg_rds" { # 하이픈(-)을 언더바(_)로 수정
  name        = "terraform-sg-rds"
  description = "Allow inbound traffic from Bastion to RDS"
  vpc_id      = aws_vpc.king_vpc.id

  tags = {
    Name = "terraform-sg-rds"
  }

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"
    # 중요: 위에서 정의한 Bastion SG를 언더바 이름으로 참조해야 함
    security_groups = [aws_security_group.terraform_sg_bastion.id]
    description     = "Allow MariaDB access from Bastion"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
