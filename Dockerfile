FROM python:3.7-slim-buster

LABEL version="2"
LABEL maintaner="Jonathan Lüdemann (jolu@trifork)"

RUN apt-get update && apt-get install -y git

WORKDIR /app

SHELL ["/bin/bash", "-c"]

RUN apt-get install ffmpeg libsm6 libxext6  -y

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Start flask server endpoint to train received data
# Start with docker run -d -p 5000:5000 <name of docker image>
ENTRYPOINT [ "python" ]

CMD ["./src/app.py" ]