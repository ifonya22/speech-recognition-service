FROM python:3.12-bullseye

WORKDIR /app
RUN pip install websockets

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt update && apt install -y ffmpeg

COPY /src /app

CMD [ "python", "-m", "main"]