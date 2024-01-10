FROM python:3.10.12

RUN mkdir /weather_bot

WORKDIR /weather_bot

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "bot.py"]
