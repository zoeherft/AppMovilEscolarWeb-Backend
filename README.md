# 🎓 Sistema de Gestión de Eventos Académicos - Backend API

Backend desarrollado con **Django REST Framework** para el sistema de gestión de eventos académicos universitarios. Proporciona APIs RESTful para la administración de usuarios y eventos académicos.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración de Base de Datos](#-configuración-de-base-de-datos)
- [Ejecución del Servidor](#-ejecución-del-servidor)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

- ✅ **CRUD completo** para Eventos Académicos
- ✅ **Gestión de usuarios** (Administradores, Maestros y Alumnos)
- ✅ **Autenticación** mediante Token Bearer
- ✅ **Control de acceso por roles** (Admin: CRUD completo, Maestros/Alumnos: solo lectura)
- ✅ **Validación de datos** en todas las operaciones
- ✅ **Tipos de eventos**: Conferencias, Talleres, Seminarios, Concursos
- ✅ **CORS habilitado** para comunicación con el Frontend

---

## 🛠 Tecnologías

| Tecnología | Versión |
|------------|---------|
| Python | 3.10+ |
| Django | 5.0.2 |
| Django REST Framework | 3.16.1 |
| MySQL/MariaDB | 8.0+ |
| PyMySQL | Latest |

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.10 o superior**
   ```bash
   python --version
   ```

2. **pip** (gestor de paquetes de Python)
   ```bash
   pip --version
   ```

3. **MySQL/MariaDB** instalado y corriendo
   ```bash
   mysql --version
   ```

4. **Virtualenv** (recomendado)
   ```bash
   pip install virtualenv
   ```

---

## 🚀 Instalación

### Paso 1: Navegar al proyecto

```bash
cd app-movil-escolar-backend
```

### Paso 2: Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄 Configuración de Base de Datos

### Paso 1: Crear la base de datos en MySQL

```sql
-- Conectarse a MySQL
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE eventos_academicos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Salir
EXIT;
```

### Paso 2: Configurar credenciales

Edita el archivo `my.cnf` con tus credenciales:

```ini
[client]
host=127.0.0.1
port = 3306
database = eventos_academicos_db
user = root
password = tu_password
default-character-set = utf8mb4
```

### Paso 3: Ejecutar migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### Paso 4: Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

---

## ▶️ Ejecución del Servidor

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000/
```

---

## 📡 Endpoints de la API

### Base URL
```
http://127.0.0.1:8000/
```

### 🔐 Autenticación

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| POST | `/login/` | Iniciar sesión | No |
| GET | `/logout/` | Cerrar sesión | Sí |

### 📅 Eventos Académicos

| Método | Endpoint | Descripción | Requiere Auth | Permisos |
|--------|----------|-------------|---------------|----------|
| GET | `/lista-eventos/` | Listar eventos (filtrado por rol) | Sí | Todos |
| GET | `/eventos/?id={id}` | Obtener evento por ID | Sí | Todos |
| POST | `/eventos/` | Crear nuevo evento | Sí | Solo Admin |
| PUT | `/eventos/` | Actualizar evento | Sí | Solo Admin |
| DELETE | `/eventos/?id={id}` | Eliminar evento | Sí | Solo Admin |
| GET | `/responsables/` | Listar responsables disponibles | Sí | Solo Admin |

### 👥 Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST/PUT/DELETE | `/admin/` | CRUD de Administradores |
| GET/POST/PUT/DELETE | `/maestros/` | CRUD de Maestros |
| GET/POST/PUT/DELETE | `/alumnos/` | CRUD de Alumnos |
| GET | `/lista-admins/` | Listar administradores |
| GET | `/lista-maestros/` | Listar maestros |
| GET | `/lista-alumnos/` | Listar alumnos |

### 📊 Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/total-usuarios/` | Total de usuarios por rol |

---

## 📅 Modelo de Evento Académico

```python
{
    "nombre_evento": "Congreso de Tecnología 2025",
    "tipo_evento": "Conferencia",  # Conferencia, Taller, Seminario, Concurso
    "fecha_realizacion": "2025-12-15",
    "hora_inicio": "09:00",
    "hora_fin": "14:00",
    "lugar": "Auditorio Principal",
    "publico_objetivo": ["Alumnos", "Maestros"],  # Array JSON
    "programa_educativo": "ICC",  # ICC, LCC, ITI (solo si público incluye Alumnos)
    "responsable": 1,  # ID del usuario responsable (Maestro o Admin)
    "descripcion": "Descripción del evento (máx 300 caracteres)",
    "cupo_maximo": 100
}
```

### Tipos de Evento
- **Conferencia**: Charlas magistrales
- **Taller**: Actividades prácticas
- **Seminario**: Sesiones de estudio
- **Concurso**: Competencias académicas

### Programas Educativos
- **ICC**: Ingeniería en Ciencias de la Computación
- **LCC**: Licenciatura en Ciencias de la Computación
- **ITI**: Ingeniería en Tecnologías de la Información

---

## 📁 Estructura del Proyecto

```
app-movil-escolar-backend/
├── app_movil_escolar_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py              # Modelos: Administradores, Maestros, Alumnos, EventosAcademicos
│   ├── serializers.py         # Serializadores para la API
│   ├── settings.py            # Configuración de Django
│   ├── urls.py                # Rutas de la API
│   ├── views/
│   │   ├── __init__.py
│   │   ├── users.py           # Vistas de Administradores
│   │   ├── maestros.py        # Vistas de Maestros
│   │   ├── alumnos.py         # Vistas de Alumnos
│   │   ├── eventos.py         # Vistas de Eventos Académicos
│   │   ├── auth.py            # Vistas de Autenticación
│   │   └── bootstrap.py
│   └── migrations/
├── static/
├── manage.py
├── requirements.txt
├── my.cnf                     # Configuración de MySQL
└── README.md
```

---

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'pymysql'"
```bash
pip install pymysql
```

### Error: "Access denied for user"
Verifica las credenciales en `my.cnf`.

### Error: "CORS blocked"
Asegúrate de que el frontend esté en `CORS_ALLOWED_ORIGINS` en `settings.py`.

---

## 👥 Autores

- **Materia**: Desarrollo de Aplicaciones Móviles
- **Semestre**: Séptimo Semestre
- **Fecha**: Noviembre 2025

---

## 📄 Licencia

Este proyecto es para fines educativos.
