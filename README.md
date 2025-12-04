# API REST - Plataforma de Eventos Escolares 📚

API desarrollada en **Django REST Framework** que proporciona los servicios backend para la plataforma de gestión de eventos escolares.

## Enlaces de Producción

| Servicio | URL |
|----------|-----|
| API Backend | https://app-eventos-backend.onrender.com |
| Aplicación Web | https://app-eventos-frontend.vercel.app |

---

## Índice

1. [Funcionalidades](#funcionalidades)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Preparación del Entorno](#preparación-del-entorno)
4. [Guía de Instalación](#guía-de-instalación)
5. [Base de Datos](#base-de-datos)
6. [Configuración del Sistema](#configuración-del-sistema)
7. [Iniciar el Servidor](#iniciar-el-servidor)
8. [Referencia de la API](#referencia-de-la-api)
9. [Publicación en Render](#publicación-en-render)
10. [Organización de Archivos](#organización-de-archivos)
11. [Resolución de Errores](#resolución-de-errores)

---

## Funcionalidades

El sistema ofrece las siguientes capacidades:

- **Administración de eventos**: Operaciones completas de creación, lectura, actualización y eliminación
- **Gestión de usuarios**: Soporte para tres tipos de usuario (Administrador, Docente, Estudiante)
- **Sistema de autenticación**: Implementación de tokens Bearer para seguridad
- **Permisos por rol**: Restricciones de acceso según el tipo de usuario
- **Validación robusta**: Verificación de datos en cada operación
- **Configuración CORS**: Comunicación segura con aplicaciones cliente
- **Archivos estáticos**: Servidos mediante WhiteNoise en producción

---

## Stack Tecnológico

| Componente | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje de programación |
| Django | 5.0.2 | Framework web |
| DRF | 3.16.1 | Construcción de APIs |
| PostgreSQL | 15+ | BD en producción |
| MySQL | 8.0+ | BD en desarrollo |
| Gunicorn | 21.2.0 | Servidor de aplicaciones |
| WhiteNoise | 6.6.0 | Manejo de estáticos |

---

## Preparación del Entorno

Antes de comenzar, asegúrate de contar con:

**Python 3.10 o superior**
```bash
python --version
```

**Gestor de paquetes pip**
```bash
pip --version
```

**MySQL Server** (únicamente para desarrollo)
```bash
mysql --version
```

---

## Guía de Instalación

### 1. Obtener el código fuente

```bash
git clone https://github.com/zoeherft/AppMovilEscolarWeb-Backend.git
cd AppMovilEscolarWeb-Backend
```

### 2. Configurar entorno virtual de Python

```bash
python -m venv venv
```

Activación en **macOS/Linux**:
```bash
source venv/bin/activate
```

Activación en **Windows**:
```bash
venv\Scripts\activate
```

### 3. Instalar paquetes necesarios

```bash
pip install -r requirements.txt
```

---

## Base de Datos

### Configuración para desarrollo (MySQL)

**Paso 1**: Crear la base de datos en MySQL
```sql
CREATE DATABASE app_movil_escolar_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

**Paso 2**: Generar archivo de configuración local

Duplica el archivo plantilla:
```bash
cp my.cnf my.cnf.local
```

Modifica `my.cnf.local` con tus datos:
```ini
[client]
host=127.0.0.1
port = 3306
database = app_movil_escolar_db
user = tu_usuario_mysql
password = tu_contraseña_mysql
default-character-set = utf8mb4
```

**Paso 3**: Aplicar migraciones
```bash
python manage.py migrate
```

---

## Configuración del Sistema

### Entorno de Desarrollo
El sistema funciona sin variables de entorno adicionales en modo desarrollo.

### Entorno de Producción (Render)

Variables requeridas:

| Nombre | Descripción | Valor de ejemplo |
|--------|-------------|------------------|
| `SECRET_KEY` | Llave secreta de Django | `clave-aleatoria-segura-123` |
| `DEBUG` | Activar depuración | `False` |
| `DATABASE_URL` | Conexión PostgreSQL | `postgres://usr:pwd@host:5432/db` |
| `VERCEL_FRONTEND_URL` | Dominio del frontend | `https://app-eventos-frontend.vercel.app` |
| `DJANGO_SUPERUSER_USERNAME` | Nombre de superusuario | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Correo de superusuario | `admin@correo.com` |
| `DJANGO_SUPERUSER_PASSWORD` | Clave de superusuario | `password-seguro` |

---

## Iniciar el Servidor

### Modo desarrollo
```bash
python manage.py runserver
```
Accede desde: http://127.0.0.1:8000/

### Modo producción
El despliegue utiliza Gunicorn según la configuración en `render.yaml`.

---

## Referencia de la API

### URLs base
- **Desarrollo**: `http://127.0.0.1:8000`
- **Producción**: `https://app-eventos-backend.onrender.com`

### Endpoints de Autenticación

| Verbo | Ruta | Función |
|-------|------|---------|
| POST | `/login/` | Autenticar usuario |
| GET | `/logout/` | Finalizar sesión |

### Endpoints de Eventos Académicos

| Verbo | Ruta | Función | Acceso |
|-------|------|---------|--------|
| GET | `/lista-eventos/` | Consultar todos los eventos | Cualquier usuario |
| GET | `/eventos/?id={id}` | Consultar evento específico | Cualquier usuario |
| POST | `/eventos/` | Registrar nuevo evento | Administrador |
| PUT | `/eventos/` | Modificar evento existente | Administrador |
| DELETE | `/eventos/?id={id}` | Eliminar evento | Administrador |

### Endpoints de Gestión de Usuarios

| Verbo | Ruta | Función |
|-------|------|---------|
| GET/POST/PUT/DELETE | `/admin/` | Operaciones sobre administradores |
| GET/POST/PUT/DELETE | `/maestros/` | Operaciones sobre docentes |
| GET/POST/PUT/DELETE | `/alumnos/` | Operaciones sobre estudiantes |

---

## Publicación en Render

**Paso 1**: Vincular tu repositorio en [render.com](https://render.com)

**Paso 2**: Definir las variables de entorno mencionadas anteriormente

**Paso 3**: El archivo `render.yaml` se encarga de:
- Configurar el servicio web con Gunicorn
- Provisionar PostgreSQL
- Ejecutar `./build.sh` durante el despliegue

**Paso 4**: Cada push a la rama principal activa un nuevo despliegue

---

## Organización de Archivos

```
AppMovilEscolarWeb-Backend/
├── app_movil_escolar_api/
│   ├── models.py           # Definición de modelos
│   ├── serializers.py      # Conversión de datos
│   ├── settings.py         # Parámetros del proyecto
│   ├── urls.py             # Definición de rutas
│   └── views/              # Lógica de negocio
├── build.sh                # Script de construcción
├── render.yaml             # Configuración Render
├── requirements.txt        # Dependencias Python
├── my.cnf                  # Plantilla MySQL
└── manage.py               # Utilidad de Django
```

---

## Resolución de Errores

### No conecta a MySQL
- Revisa que `my.cnf.local` tenga los datos correctos
- Confirma que el servicio MySQL esté activo

### Respuesta 401 de la API
- Asegúrate de incluir el token Bearer en los headers
- El token pudo expirar, inicia sesión nuevamente

### Problemas de CORS
- Verifica la variable `CORS_ALLOWED_ORIGINS` en `settings.py`
- En producción, confirma que `VERCEL_FRONTEND_URL` esté configurado

---

## Información del Proyecto

- **Asignatura**: Desarrollo de Aplicaciones Móviles
- **Nivel**: Universitario
- **Periodo**: Noviembre 2025

---

## Términos de Uso

Este proyecto fue desarrollado con fines académicos. Todos los derechos reservados.
