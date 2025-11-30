#!/usr/bin/env bash
# Script de construcción para Render

set -o errexit  # Salir si hay error

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

# Crear o actualizar superusuario (usa variables de entorno)
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_superuser': True, 'is_staff': True})
user.set_password(password)
user.email = email
user.is_superuser = True
user.is_staff = True
user.save()

if created:
    print(f'Superusuario "{username}" creado exitosamente')
else:
    print(f'Superusuario "{username}" actualizado exitosamente')
EOF

