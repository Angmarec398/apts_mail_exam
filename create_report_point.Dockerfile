# Указываем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app_create_to_db

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем нужные файлы для контейнера
COPY create_report_point.py .
COPY model.py .

# Указываем команду для запуска при старте контейнера
CMD ["python", "create_report_point.py"]
