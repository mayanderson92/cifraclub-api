FROM python:3.8-slim-bullseye

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python3", "api.py"]
