FROM python:3.8-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
  pylint \
  pylint_flask \
  pytest \
  pytest-cov

COPY app/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

CMD ["python3", "api.py"]
