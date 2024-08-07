FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/staticfiles

CMD ["gunicorn", "weather_to_music.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]