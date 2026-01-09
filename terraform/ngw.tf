# 탄력적(Elastic) IP
resource "aws_eip" "terraform-eip" {
  domain = "vpc"
}

# NAT 게이트웨이
resource "aws_nat_gateway" "terraform_ngw" {
  allocation_id = aws_eip.terraform-eip.id
  subnet_id     = aws_subnet.PUB_subnet_2A.id
  tags = {
    "Name" = "terraform-ngw"
  }
}
