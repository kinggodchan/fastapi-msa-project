resource "aws_internet_gateway" "terraform_igw" {
  vpc_id = aws_vpc.king_vpc.id

  tags = {
    Name = "king-igw" # AWS 태그 값은 하이픈 OK
  }
}
