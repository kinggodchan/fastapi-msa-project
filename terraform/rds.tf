# 1. RDS 서브넷 그룹 생성
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "terraform-rds-subnet-group"
  subnet_ids = [aws_subnet.PRI_subnet_2A.id, aws_subnet.PRI_subnet_2C.id] #

  tags = {
    Name = "terraform-rds-subnet-group"
  }
}

# 2. MariaDB Parameter Group 설정
resource "aws_db_parameter_group" "mariadb_param" {
  name   = "terraform-mariadb-parameter-group"
  family = "mariadb11.4" #

  parameter {
    name  = "max_connections"
    value = "150"
  }

  parameter {
    name  = "time_zone"
    value = "Asia/Seoul"
  }

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }

  parameter {
    name  = "collation_server"
    value = "utf8mb4_unicode_ci"
  }
}

# 3. RDS 인스턴스 생성
resource "aws_db_instance" "mariadb_rds" {
  identifier        = "terraform-mariadb-rds"
  allocated_storage = 20
  engine            = "mariadb"
  engine_version    = "11.4"
  instance_class    = "db.t3.micro"

  # ✅ 수정 완료: DB 이름을 수집기 코드와 일치시킴
  db_name = "real_estate"

  # ✅ 사용자 및 비밀번호 설정 (collector.py와 일치 권장)
  username = "test01"
  password = "password123" #

  parameter_group_name = aws_db_parameter_group.mariadb_param.name
  db_subnet_group_name = aws_db_subnet_group.rds_subnet_group.name

  # 보안 그룹 연결 (언더바(_) 형식 참조)
  vpc_security_group_ids = [aws_security_group.terraform_sg_rds.id] #

  # 연습용이므로 삭제 시 스냅샷 생성 건너뛰기
  skip_final_snapshot = true #

  tags = {
    Name = "terraform-mariadb-rds"
  }
}

