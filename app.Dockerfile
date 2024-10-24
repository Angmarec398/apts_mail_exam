# Указываем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app_create

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
#EXPOSE 8005

# Run the application.
CMD ["python","app.py"]