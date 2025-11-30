#!/usr/bin/env bash
# Script de construcción para Render

set -o errexit  # Salir si hay error

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate
