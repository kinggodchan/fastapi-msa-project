# 🚀 FastAPI MSA Kubernetes Project

FastAPI와 MariaDB를 이용한 마이크로서비스 아키텍처(MSA) 프로젝트입니다. 
쿠버네티스(k8s) 환경에서 MetalLB와 Nginx Ingress를 통해 배포되었습니다.

## 🏗 시스템 아키텍처


* **Auth Service**: 사용자 인증 및 JWT 토큰 발급
* **Board Service**: 게시판 포스팅 및 조회
* **Frontend**: Nginx 기반 정적 웹 페이지
* **Database**: MariaDB (각 서비스별 논리적 DB 분리)
* **Ingress**: Path-based Routing (`/api/auth`, `/api/board`)

## 🛠 기술 스택
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: MariaDB 11
- **Container**: Docker
- **Orchestration**: Kubernetes (v1.29)
- **Ingress**: Nginx Ingress Controller
- **Network**: MetalLB

## 🚀 배포 방법
1. **데이터베이스 설정**:
   ```bash kubectl apply -f mariadb/

