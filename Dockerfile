FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENTRYPOINT ["gunicorn", "weather_to_music.wsgi:application"]