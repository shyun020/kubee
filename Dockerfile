FROM ubuntu:22.04

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# 파이썬 라이브러리 설치
RUN pip3 install flask PyJWT

# 앱 파일 복사
COPY app.py /app/app.py

# 필수 디렉토리 생성 (앱에서 사용하는 uploads 디렉토리)
RUN mkdir -p /app/uploads

# 작업 디렉토리 설정
WORKDIR /app

# 앱 실행
CMD ["python3", "app.py"]
