# Используем официальный образ Python 3.10.13
FROM python:3.10.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Указываем команду запуска (если start.sh)
CMD ["bash", "start.sh"]
