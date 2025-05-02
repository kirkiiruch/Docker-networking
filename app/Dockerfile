FROM python:3.9-slim

WORKDIR /app

# Устанавливаем wait-for-it
RUN apt-get update && apt-get install -y curl && \
    curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Копируем requirements.txt отдельно для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY app.py .
COPY templates/ templates/

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]