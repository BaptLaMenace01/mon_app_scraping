FROM python:3.10-slim

# Dépendances système (compatibles ARM64)
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 ca-certificates chromium-driver chromium

# Variables d'environnement pour Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
