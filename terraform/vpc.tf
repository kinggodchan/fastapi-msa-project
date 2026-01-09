resource "aws_vpc" "king_vpc" {
  cidr_block           = "10.12.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    "Name" = "king-vpc"
  }
}
