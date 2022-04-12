# syntax=docker/dockerfile:1.3
FROM python:3.7-slim-buster

LABEL version="2"
LABEL maintaner="Jonathan Lüdemann (jolu@trifork)"

RUN apt-get update && apt-get install -y git

SHELL ["/bin/bash", "-c"]

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt /
COPY donkeycar.txt /

RUN pip install -r /requirements.txt
RUN pip install -r /donkeycar.txt

COPY --chmod=777 . /app
WORKDIR /app

# Start flask server endpoint through Gunicorn to train received data
# Start with docker run -d -p 5000:5000 <name of docker image>
# Need elevated permissions: u+rwx 
# docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "./gunicorn.sh": permission denied: unknown.
ENTRYPOINT ["./gunicorn.sh"]