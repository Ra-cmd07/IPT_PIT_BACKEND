FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=kitchen_system.settings

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@admin.com').exists() or User.objects.create_superuser('admin@admin.com', 'admin@admin.com', 'password123')\" && gunicorn kitchen_system.wsgi:application --bind 0.0.0.0:8000 --workers 3"]