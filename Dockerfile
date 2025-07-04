# Используем образ с поддержкой CUDA для PyTorch, если нужен GPU, или CPU-образ
FROM pytorch/pytorch:2.3.0-cuda11.8-cudnn8-runtime

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install -r requirements.txt

# Копируем весь root
COPY . .

# Указываем что app.py - flask приложение
ENV FLASK_APP=app.py


# Открываем порт для Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]