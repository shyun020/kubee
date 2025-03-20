FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install flask

COPY app.py /app/app.py

WORKDIR /app

CMD ["python3", "app.py"]
