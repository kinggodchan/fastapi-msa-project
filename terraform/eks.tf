# EKS Cluster IAM Role 생성
resource "aws_iam_role" "terraform_eks_cluster_role" {
  name = "terraform-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}

# IAM Role에 정책 부착
resource "aws_iam_role_policy_attachment" "terraform_eks_cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.terraform_eks_cluster_role.name
}

resource "aws_iam_role_policy_attachment" "terraform_eks_cluster_AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.terraform_eks_cluster_role.name
}

# EKS Cluster 생성
resource "aws_eks_cluster" "terraform_eks_cluster" {
  name     = "terraform-eks-cluster"
  role_arn = aws_iam_role.terraform_eks_cluster_role.arn

  version = "1.31" # 1.32보다는 현재 가장 안정적으로 쓰이는 1.31을 권장합니다.

  vpc_config {
    # 📍 사용자님의 서브넷 이름으로 수정 완료
    subnet_ids              = [aws_subnet.PRI_subnet_2A.id, aws_subnet.PRI_subnet_2C.id]
    endpoint_public_access  = true
    endpoint_private_access = false
    # 📍 11번에서 만든 보안그룹 이름으로 수정 완료
    security_group_ids = [aws_security_group.terraform_sg_eks_nodes.id]
  }

  depends_on = [
    aws_iam_role_policy_attachment.terraform_eks_cluster_AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.terraform_eks_cluster_AmazonEKSVPCResourceController,
  ]
}
