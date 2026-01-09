resource "aws_instance" "terraform_pub_ec2_bastion_2a" { # 리소스 식별자도 언더바(_)로 수정
  ami           = "ami-056a29f2eddc40520"
  instance_type = "t2.micro"

  # 중요: 07번 파일에서 수정한 보안 그룹 이름을 언더바(_)로 참조해야 합니다.
  vpc_security_group_ids = [aws_security_group.terraform_sg_bastion.id]

  # 03번 파일에서 정의한 서브넷 이름과 매칭
  subnet_id = aws_subnet.PUB_subnet_2A.id

  key_name                    = "king-01-ec2"
  associate_public_ip_address = true

  root_block_device {
    volume_size = "8"
    volume_type = "gp2"
    tags = {
      "Name" = "terraform-pub-ec2-bastion-2a"
    }
  }

  tags = {
    "Name" = "terraform-pub-ec2-bastion-2a" # AWS 콘솔 태그는 하이픈(-) 유지
  }
}
