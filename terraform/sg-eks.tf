
# 1.EKS 노드 그룹 보안 그룹
resource "aws_security_group" "terraform_sg_eks_nodes" {
  name        = "terraform-sg-eks-nodes"
  description = "Security group for EKS worker nodes"
  vpc_id      = aws_vpc.king_vpc.id # 수정 완료

  # 노드 내부 통신 및 로드밸런서에서의 트래픽 허용 (0-65535 권장)
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for ping"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "terraform-sg-eks-nodes" }
}
