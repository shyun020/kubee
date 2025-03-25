FROM ubuntu:22.04

# 시스템 패키지 업데이트 및 Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# 필요한 파이썬 패키지 설치
RUN pip3 install flask PyJWT

# 앱 복사
COPY app.py /app/app.py

# 작업 디렉토리 설정
WORKDIR /app

# 컨테이너 실행 시 실행할 명령
CMD ["python3", "app.py"]
