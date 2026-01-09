# Public Subnet - 2a
resource "aws_subnet" "PUB_subnet_2A" {
  vpc_id                  = aws_vpc.king_vpc.id
  cidr_block              = "10.12.1.0/24"
  availability_zone       = "ap-northeast-2a"
  map_public_ip_on_launch = true

  tags = {
    Name                                          = "PUB_subnet_2A"
    "kubernetes.io/role/elb"                      = "1"
    "kubernetes.io/cluster/terraform-eks-cluster" = "shared"
  }
}

# Public Subnet - 2c
resource "aws_subnet" "PUB_subnet_2C" {
  vpc_id                  = aws_vpc.king_vpc.id
  cidr_block              = "10.12.2.0/24"
  availability_zone       = "ap-northeast-2c"
  map_public_ip_on_launch = true

  tags = {
    Name                                          = "PUB_subnet_2C"
    "kubernetes.io/role/elb"                      = "1"
    "kubernetes.io/cluster/terraform-eks-cluster" = "shared"
  }
}

# Private Subnet - 2a
resource "aws_subnet" "PRI_subnet_2A" {
  vpc_id            = aws_vpc.king_vpc.id
  cidr_block        = "10.12.11.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name                                          = "PRI_subnet_2A"
    "kubernetes.io/role/internal-elb"             = "1"
    "kubernetes.io/cluster/terraform-eks-cluster" = "shared"
  }
}

# Private Subnet - 2c
resource "aws_subnet" "PRI_subnet_2C" {
  vpc_id            = aws_vpc.king_vpc.id
  cidr_block        = "10.12.12.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name                                          = "PRI_subnet_2C"
    "kubernetes.io/role/internal-elb"             = "1"
    "kubernetes.io/cluster/terraform-eks-cluster" = "shared"
  }
}
