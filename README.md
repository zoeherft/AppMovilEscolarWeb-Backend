# 🎓 Sistema de Gestión de Eventos Académicos - Backend API

Backend desarrollado con **Django REST Framework** para el sistema de gestión de eventos académicos universitarios. Proporciona APIs RESTful para la administración de usuarios y eventos académicos.

## 🌐 Despliegue

- **Producción**: [https://app-eventos-backend.onrender.com](https://app-eventos-backend.onrender.com)
- **Frontend**: [https://app-eventos-frontend.vercel.app](https://app-eventos-frontend.vercel.app)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración de Base de Datos](#-configuración-de-base-de-datos)
- [Variables de Entorno](#-variables-de-entorno)
- [Ejecución](#-ejecución)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Despliegue en Render](#-despliegue-en-render)

---

## ✨ Características

- ✅ **CRUD completo** para Eventos Académicos
- ✅ **Gestión de usuarios** (Administradores, Maestros y Alumnos)
- ✅ **Autenticación** mediante Token Bearer
- ✅ **Control de acceso por roles**
- ✅ **Validación de datos** en todas las operaciones
- ✅ **CORS configurado** para comunicación segura con el Frontend
- ✅ **WhiteNoise** para servir archivos estáticos en producción

---

## 🛠 Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| Django | 5.0.2 | Framework web |
| Django REST Framework | 3.16.1 | APIs REST |
| PostgreSQL | 15+ | Base de datos (producción) |
| MySQL | 8.0+ | Base de datos (desarrollo) |
| Gunicorn | 21.2.0 | Servidor WSGI |
| WhiteNoise | 6.6.0 | Archivos estáticos |

---

## 📦 Requisitos Previos

1. **Python 3.10+**
   ```bash
   python --version
   ```

2. **pip**
   ```bash
   pip --version
   ```

3. **MySQL** (solo para desarrollo local)
   ```bash
   mysql --version
   ```

---

## 🚀 Instalación

### Paso 1: Clonar y navegar

```bash
git clone https://github.com/ivanblueberry/app-eventos-backend.git
cd app-movil-escolar-backend
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄 Configuración de Base de Datos

### Para desarrollo local (MySQL)

1. **Crear la base de datos:**
   ```sql
   CREATE DATABASE app_movil_escolar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Crear archivo de configuración:**
   
   Copia `my.cnf` a `my.cnf.local` y edita con tus credenciales:
   ```bash
   cp my.cnf my.cnf.local
   ```
   
   Edita `my.cnf.local`:
   ```ini
   [client]
   host=127.0.0.1
   port = 3306
   database = app_movil_escolar_db
   user = tu_usuario
   password = tu_contraseña
   default-character-set = utf8mb4
   ```

3. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

---

## 🔐 Variables de Entorno

### Desarrollo
No se requieren variables de entorno para desarrollo local.

### Producción (Render)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `tu-clave-secreta-muy-larga` |
| `DEBUG` | Modo debug | `False` |
| `DATABASE_URL` | URL de PostgreSQL | `postgres://user:pass@host:5432/db` |
| `VERCEL_FRONTEND_URL` | URL del frontend | `https://app-eventos-frontend.vercel.app` |
| `DJANGO_SUPERUSER_USERNAME` | Usuario admin | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Email admin | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD` | Contraseña admin | `tu-password-seguro` |

---

## ▶️ Ejecución

### Desarrollo
```bash
python manage.py runserver
# Disponible en: http://127.0.0.1:8000/
```

### Producción
El servidor usa Gunicorn configurado en `render.yaml`.

---

## 📡 Endpoints de la API

### Base URL
- **Local**: `http://127.0.0.1:8000`
- **Producción**: `https://app-eventos-backend.onrender.com`

### 🔐 Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/login/` | Iniciar sesión |
| GET | `/logout/` | Cerrar sesión |

### 📅 Eventos

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/lista-eventos/` | Listar eventos | Todos |
| GET | `/eventos/?id={id}` | Obtener evento | Todos |
| POST | `/eventos/` | Crear evento | Solo Admin |
| PUT | `/eventos/` | Actualizar evento | Solo Admin |
| DELETE | `/eventos/?id={id}` | Eliminar evento | Solo Admin |

### 👥 Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST/PUT/DELETE | `/admin/` | CRUD Administradores |
| GET/POST/PUT/DELETE | `/maestros/` | CRUD Maestros |
| GET/POST/PUT/DELETE | `/alumnos/` | CRUD Alumnos |

---

## 🚀 Despliegue en Render

1. **Conectar repositorio** en [render.com](https://render.com)

2. **Configurar variables de entorno** (ver sección anterior)

3. **El archivo `render.yaml`** configura automáticamente:
   - Web Service con Gunicorn
   - Base de datos PostgreSQL
   - Build command: `./build.sh`

4. **Push a main** para desplegar automáticamente

---

## 📁 Estructura del Proyecto

```
app-movil-escolar-backend/
├── app_movil_escolar_api/
│   ├── models.py           # Modelos de datos
│   ├── serializers.py      # Serializadores
│   ├── settings.py         # Configuración
│   ├── urls.py             # Rutas
│   └── views/              # Controladores
├── build.sh                # Script de build para Render
├── render.yaml             # Configuración de Render
├── requirements.txt        # Dependencias
├── my.cnf                  # Plantilla de config MySQL
└── manage.py
```

---

## 🔧 Solución de Problemas

### Error de conexión a MySQL
- Verifica que `my.cnf.local` tenga las credenciales correctas
- Asegúrate de que MySQL esté corriendo

### Error 401 en API
- Verifica que el token Bearer esté en el header
- El token puede haber expirado, vuelve a hacer login

### CORS Error
- Verifica `CORS_ALLOWED_ORIGINS` en `settings.py`
- En producción, configura `VERCEL_FRONTEND_URL`

---

## 👥 Autores

- **Materia**: Desarrollo de Aplicaciones Móviles
- **Institución**: Universidad
- **Fecha**: Noviembre 2025

---

## 📄 Licencia

Proyecto educativo - Todos los derechos reservados.
