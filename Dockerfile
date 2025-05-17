# Используем образ Python с поддержкой сборки C-расширений
FROM python:3.13-slim

# Установка зависимостей для сборки aiohttp и других C-зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]