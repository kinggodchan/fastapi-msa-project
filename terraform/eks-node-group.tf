# 1. Node Group IAM Role 생성
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

# 2. IAM Role에 기본 정책 추가
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

# 3. S3 접근을 위한 추가 IAM Policy 생성
resource "aws_iam_policy" "node_s3_policy" {
  name        = "terraform-sg-eks-s3-access"
  description = "Allow EKS nodes to access model S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.model_bucket.arn}",
          "${aws_s3_bucket.model_bucket.arn}/*"
        ]
      }
    ]
  })
}

# 4. S3 Policy를 Role에 연결
resource "aws_iam_role_policy_attachment" "node_s3_attach" {
  policy_arn = aws_iam_policy.node_s3_policy.arn
  role       = aws_iam_role.terraform_eks_node_group_role.name
}

# 5. Node Group 생성 (S3 권한 의존성 추가)
resource "aws_eks_node_group" "terraform_eks_node_group" {
  cluster_name    = aws_eks_cluster.terraform_eks_cluster.name
  node_group_name = "terraform-eks-node-group"
  node_role_arn   = aws_iam_role.terraform_eks_node_group_role.arn
  subnet_ids      = [aws_subnet.PRI_subnet_2A.id, aws_subnet.PRI_subnet_2C.id]

  tags = {
    "k8s.io/cluster-autoscaler/enabled"               = "true"
    "k8s.io/cluster-autoscaler/terraform-eks-cluster" = "owned"
  }

  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 2
  }

  ami_type       = "AL2_x86_64"
  instance_types = ["t3.medium"]
  disk_size      = 20

  # 핵심: 모든 정책 연결이 완료된 후 노드 그룹이 생성되도록 지정
  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
    aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_s3_attach # 추가됨
  ]
}
