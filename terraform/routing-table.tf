# 라우팅 테이블
resource "aws_route_table" "terraform_pub_rt" {
  vpc_id = aws_vpc.king_vpc.id
  tags   = { "Name" = "terraform-pub-rt" }
}

resource "aws_route_table" "terraform_pri_rt" {
  vpc_id = aws_vpc.king_vpc.id
  tags   = { "Name" = "terraform-pri-rt" }
}

# 라우팅 규칙
resource "aws_route" "pub_route" {
  route_table_id         = aws_route_table.terraform_pub_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.terraform_igw.id
}

resource "aws_route" "pri_route" {
  route_table_id         = aws_route_table.terraform_pri_rt.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.terraform_ngw.id
}

# 서브넷 연결
resource "aws_route_table_association" "pub_2a" {
  subnet_id      = aws_subnet.PUB_subnet_2A.id
  route_table_id = aws_route_table.terraform_pub_rt.id
}

resource "aws_route_table_association" "pub_2c" {
  subnet_id      = aws_subnet.PUB_subnet_2C.id
  route_table_id = aws_route_table.terraform_pub_rt.id
}

resource "aws_route_table_association" "pri_2a" {
  subnet_id      = aws_subnet.PRI_subnet_2A.id
  route_table_id = aws_route_table.terraform_pri_rt.id
}

resource "aws_route_table_association" "pri_2c" {
  subnet_id      = aws_subnet.PRI_subnet_2C.id
  route_table_id = aws_route_table.terraform_pri_rt.id
}
