# Node Group IAM Role 생성
resource "aws_iam_role" "terraform_eks_node_group_role" {
  name = "terraform-eks-node-group-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

# IAM Role에 정책 추가
resource "aws_iam_role_policy_attachment" "AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.terraform_eks_node_group_role.name
}

resource "aws_iam_role_policy_attachment" "AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.terraform_eks_node_group_role.name
}

resource "aws_iam_role_policy_attachment" "AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.terraform_eks_node_group_role.name
}

# Node Group 생성
resource "aws_eks_node_group" "terraform_eks_node_group" {
  # 📍 위에서 정의한 클러스터 이름 참조
  cluster_name    = aws_eks_cluster.terraform_eks_cluster.name
  node_group_name = "terraform-eks-node-group"
  node_role_arn   = aws_iam_role.terraform_eks_node_group_role.arn

  # 📍 사용자님의 프라이빗 서브넷 이름으로 수정 완료
  subnet_ids = [aws_subnet.PRI_subnet_2A.id, aws_subnet.PRI_subnet_2C.id]

  tags = {
    "k8s.io/cluster-autoscaler/enabled"               = "true"
    "k8s.io/cluster-autoscaler/terraform-eks-cluster" = "owned"
  }

  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 2
  }

  ami_type = "AL2_x86_64"
  # 📍 t3.large는 비용이 많이 발생할 수 있어 학습용으로는 t3.medium을 추천하지만, 
  # 무거운 앱이라면 그대로 large를 쓰셔도 됩니다.
  instance_types = ["t3.medium"]
  disk_size      = 20

  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
    aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy
  ]
}
