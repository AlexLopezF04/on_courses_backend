<div align="center">

# 🎓 OnCourses API

**Plataforma de Cursos Online de Tecnología — Backend**

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-A30000?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-File%20Upload-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

</div>

## 📋 Tabla de Contenidos

- [Información General](#-información-general)
- [Arquitectura](#-arquitectura)
- [Modelo de Datos](#-modelo-de-datos)
- [Instalación Local](#-instalación-local)
- [Uso de la API](#-uso-de-la-api)
- [Endpoints](#-endpoints)
- [Despliegue en Producción](#-despliegue-en-producción)
- [Tecnologías](#-tecnologías)

---

## 📖 Información General

**OnCourses** es una plataforma de cursos online enfocada en tecnología. Este repositorio contiene el **backend** completo desarrollado con Django y Django REST Framework, diseñado para ser consumido por aplicaciones web (React/Next.js) y móviles (Flutter/React Native).

### ✨ Funcionalidades Principales

<div align="center">

| # | Módulo | Descripción |
|---|--------|-------------|
| 01 | 👤 **Usuarios y Auth** | Registro, login JWT, 3 roles (estudiante, profesor, admin), perfiles |
| 02 | 📚 **Cursos** | Categorías, cursos, módulos, lecciones, recursos descargables |
| 03 | 💬 **Comunidad** | Foros por curso, anuncios, comentarios con respuestas anidadas |
| 04 | 📈 **Progreso** | Inscripciones, avance por lección, banco de preguntas, exámenes, certificados |
| 05 | 🏆 **Gamificación** | Logros, reseñas y calificaciones de cursos |
| 06 | 🛒 **Comercial** | Carrito de compras, cupones de descuento, órdenes, tickets de soporte |

</div>

---

## 🏗 Arquitectura

El proyecto sigue una **arquitectura modular** basada en 6 aplicaciones Django independientes:

```
on_courses_backend/
├── config/                  # Configuración central
│   ├── settings.py          # Base de datos, JWT, DRF, CORS, Email
│   ├── urls.py              # Enrutador principal
│   ├── wsgi.py              # Entry point para Gunicorn
│   └── pagination.py        # Paginación personalizada
├── apps/
│   ├── users/               # Módulo 1: Usuarios (4 tablas)
│   ├── courses/             # Módulo 2: Cursos (5 tablas)
│   ├── community/           # Módulo 3: Comunidad (4 tablas)
│   ├── progress/            # Módulo 4: Progreso (9 tablas)
│   ├── gamification/        # Módulo 5: Gamificación (3 tablas)
│   └── commercial/          # Módulo 6: Comercial (7 tablas)
├── .env                     # Variables de entorno
├── manage.py                # CLI de Django
└── pyproject.toml           # Dependencias (uv)
```

---

## 🗄 Modelo de Datos

**32 tablas** distribuidas en 6 módulos, más 11 tablas del framework Django = **43 tablas en PostgreSQL**.

```mermaid
flowchart TD
    subgraph USR["👤 Usuarios"]
        U["User"]
        SP["StudentProfile"]
        PP["ProfessorProfile"]
        AL["AccessLog"]
    end
    subgraph CRS["📚 Cursos"]
        CAT["Category"]
        CO["Course"]
        MO["Module"]
        LE["Lesson"]
        RE["Resource"]
    end
    subgraph COM["💬 Comunidad"]
        FT["ForumThread"]
        FP["ForumPost"]
        AN["Announcement"]
        LC["LessonComment"]
    end
    subgraph PRO["📈 Progreso"]
        EN["Enrollment"]
        LP["LessonProgress"]
        QB["QuestionBank"]
        QO["QuestionOption"]
        EX["Exam"]
        EQ["ExamQuestion"]
        EA["ExamAttempt"]
        AA["AttemptAnswer"]
        CE["Certificate"]
    end
    subgraph GAM["🏆 Gamificación"]
        AC["Achievement"]
        UA["UserAchievement"]
        RV["Review"]
    end
    subgraph COMER["🛒 Comercial"]
        CT["Cart"]
        CI["CartItem"]
        CP["Coupon"]
        OD["Order"]
        OI["OrderItem"]
        ST["SupportTicket"]
        SM["SupportMessage"]
    end

    U --- SP & PP & AL
    U --- FT & FP & LC
    U --- EN & LP & EA & CE
    U --- UA & RV
    U --- OD & ST & SM
    U -.- CT

    CAT --- CO
    PP --- CO
    CO --- MO & FT & AN
    CO --- EN & QB & EX
    CO --- RV
    CO --- OI
    CO -.- CI

    MO --- LE
    LE --- RE & LC & LP

    FT --- FP
    QB --- QO & EQ
    EX --- EQ & EA
    EA --- AA
    AA --- QO

    AC --- UA
    EN --- CE

    CT --- CI
    CP --- OD
    OD --- OI
    ST --- SM
```

> 💡 **Nota:** También puedes visualizar el diagrama completo con campos en [dbdiagram.io](https://dbdiagram.io) importando el script [`dbdiagram.txt`](dbdiagram.txt).

<div align="center">

| Módulo | Tablas |
|--------|--------|
| 👤 **Usuarios** | `User`, `StudentProfile`, `ProfessorProfile`, `AccessLog` |
| 📚 **Cursos** | `Category`, `Course`, `Module`, `Lesson`, `Resource` |
| 💬 **Comunidad** | `ForumThread`, `ForumPost`, `Announcement`, `LessonComment` |
| 📈 **Progreso** | `Enrollment`, `LessonProgress`, `QuestionBank`, `QuestionOption`, `Exam`, `ExamQuestion`, `ExamAttempt`, `AttemptAnswer`, `Certificate` |
| 🏆 **Gamificación** | `Achievement`, `UserAchievement`, `Review` |
| 🛒 **Comercial** | `Cart`, `CartItem`, `Coupon`, `Order`, `OrderItem`, `SupportTicket`, `SupportMessage` |

</div>

---

## 🚀 Instalación Local

### Prerrequisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- PostgreSQL 16+

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlexLopezF04/on_courses_backend.git
cd on_courses_backend

# 2. Crear la base de datos en PostgreSQL
psql -U postgres
CREATE DATABASE nombre_bd;
CREATE USER nombre_usuario WITH PASSWORD 'tu_contraseña_segura';
ALTER ROLE nombre_usuario SET client_encoding TO 'utf8';
ALTER ROLE nombre_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE nombre_usuario SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE nombre_bd TO nombre_usuario;
ALTER USER nombre_usuario CREATEDB;
\q

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de base de datos

# 4. Instalar dependencias
uv sync

# 5. Ejecutar migraciones
uv run python manage.py migrate

# 6. Crear superusuario
uv run python manage.py createsuperuser

# 7. Iniciar servidor de desarrollo
uv run python manage.py runserver
```

### Variables de Entorno

```env
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (usar las credenciales que creaste en el paso anterior)
DB_NAME=nombre_bd
DB_USER=nombre_usuario
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True

# Email (opcional en desarrollo)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Ejecutar Tests

```bash
# Todos los tests
uv run python manage.py test

# Tests por módulo
uv run python manage.py test apps.users.tests
uv run python manage.py test apps.courses.tests
uv run python manage.py test apps.progress.tests
```

---

## 📡 Uso de la API

### Obtener Token JWT

```bash
# 1. Registrar un usuario
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "estudiante1",
    "email": "estudiante1@test.com",
    "password": "Pass1234!",
    "password_confirm": "Pass1234!"
  }'

# 2. Iniciar sesión (obtener token)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "estudiante1",
    "password": "Pass1234!"
  }'

# Respuesta:
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Usar Endpoints Protegidos

```bash
# Incluir el token en el header Authorization
curl http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Ejemplos de Peticiones

```bash
# Listar cursos (público)
curl http://localhost:8000/api/courses/

# Buscar cursos por título
curl "http://localhost:8000/api/courses/?search=django"

# Filtrar por precio
curl "http://localhost:8000/api/courses/?min_price=10&max_price=100"

# Paginación
curl "http://localhost:8000/api/courses/?page=2"

# Crear curso (requiere profesor/admin)
curl -X POST http://localhost:8000/api/courses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "category": 1,
    "title": "Django REST Framework",
    "slug": "django-rest-framework",
    "price": "49.99"
  }'

# Inscribirse a un curso
curl -X POST http://localhost:8000/api/enrollments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"course": 1}'

# Agregar ítem al carrito
curl -X POST http://localhost:8000/api/cart-items/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"course": 1}'
```

---

## 📍 Endpoints

### 🔐 Autenticación

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 01 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/health/` | 🌐 Público | Verificar servidor |
| 02 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/auth/register/` | 🌐 Público | Registrar usuario |
| 03 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/auth/login/` | 🌐 Público | Iniciar sesión (JWT) |
| 04 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/auth/refresh/` | 🌐 Público | Refrescar token |

</div>

### 👤 Usuarios

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 05 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/users/` | 👑 Admin | Listar usuarios |
| 06 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/users/{id}/` | 🔑 Owner/Admin | Ver perfil |
| 07 | ![](https://img.shields.io/badge/PATCH-FFC107?style=flat-square) | `/api/users/{id}/` | 🔑 Owner/Admin | Actualizar perfil |
| 08 | ![](https://img.shields.io/badge/DELETE-DC3545?style=flat-square) | `/api/users/{id}/` | 👑 Admin | Eliminar usuario |

</div>

### 📚 Cursos

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 09 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/categories/` | 🌐 Público | Listar categorías |
| 10 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/categories/` | 👑 Admin | Crear categoría |
| 11 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/courses/` | 🌐 Público | Listar cursos |
| 12 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/courses/` | 🎓 Profesor/Admin | Crear curso |
| 13 | ![](https://img.shields.io/badge/PATCH-FFC107?style=flat-square) | `/api/courses/{id}/` | 🔑 Owner/Admin | Actualizar curso |
| 14 | ![](https://img.shields.io/badge/DELETE-DC3545?style=flat-square) | `/api/courses/{id}/` | 👑 Admin | Eliminar curso |
| 15 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/modules/` | 🎓 Profesor/Admin | Crear módulo |
| 16 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/lessons/` | 🎓 Profesor/Admin | Crear lección |
| 17 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/resources/` | 🎓 Profesor/Admin | Subir recurso |

</div>

### 💬 Comunidad

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 18 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/forum-threads/` | 🌐 Público | Listar hilos |
| 19 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/forum-threads/` | 🔒 Autenticado | Crear hilo |
| 20 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/forum-posts/` | 🔒 Autenticado | Responder hilo |
| 21 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/announcements/` | 🔒 Autenticado | Ver anuncios |
| 22 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/announcements/` | 🎓 Profesor/Admin | Crear anuncio |
| 23 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/lesson-comments/` | 🔒 Autenticado | Comentar lección |

</div>

### 📈 Progreso

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 24 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/enrollments/` | 🔒 Autenticado | Inscribirse a curso |
| 25 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/lesson-progress/` | 🔒 Autenticado | Actualizar progreso |
| 26 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/exam-attempts/` | 🔒 Autenticado | Iniciar intento |
| 27 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/exam-attempts/{id}/submit/` | 🔒 Autenticado | Entregar respuestas |
| 28 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/certificates/` | 👑 Admin | Listar certificados |

</div>

### 🏆 Gamificación

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 29 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/achievements/` | 🌐 Público | Listar logros |
| 30 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/achievements/` | 👑 Admin | Crear logro |
| 31 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/reviews/` | 🔒 Autenticado | Calificar curso |

</div>

### 🛒 Comercial

<div align="center">

| # | Método | Ruta | Acceso | Descripción |
|---|---|---|---|---|
| 32 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/carts/mine/` | 🔒 Autenticado | Ver mi carrito |
| 33 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/cart-items/` | 🔒 Autenticado | Agregar curso |
| 34 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/coupons/validate/?code=X` | 🌐 Público | Validar cupón |
| 35 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/orders/` | 🔒 Autenticado | Crear orden |
| 36 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/orders/{id}/pay/` | 🔒 Autenticado | Pagar orden |
| 37 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/support-tickets/` | 🔒 Autenticado | Abrir ticket |
| 38 | ![](https://img.shields.io/badge/POST-198754?style=flat-square) | `/api/support-tickets/{id}/add_message/` | 🔒 Autenticado | Responder ticket |

</div>

### 📖 Documentación

<div align="center">

| # | Método | Ruta | Descripción |
|---|---|---|---|
| 39 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/docs/` | Swagger UI (interactivo) |
| 40 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/redoc/` | ReDoc (lectura) |
| 41 | ![](https://img.shields.io/badge/GET-0D6EFD?style=flat-square) | `/api/schema/` | Schema OpenAPI (JSON) |

</div>

---

## ☁ Despliegue en Producción

### Configuración del VPS (Ubuntu 22.04+)

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3.13 python3.13-venv nginx postgresql postgresql-contrib

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuración de PostgreSQL

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE nombre_bd;
CREATE USER nombre_usuario WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE nombre_bd TO nombre_usuario;
ALTER USER nombre_usuario CREATEDB;
\q
```

### Configuración de Gunicorn

Crear archivo `/etc/systemd/system/oncourses.service`:

```ini
[Unit]
Description=OnCourses API - Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/on_courses_backend
EnvironmentFile=/var/www/on_courses_backend/.env
ExecStart=/var/www/on_courses_backend/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/on_courses_backend/oncourses.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl start oncourses
sudo systemctl enable oncourses
```

### Configuración de Nginx

Crear archivo `/etc/nginx/sites-available/oncourses`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location /static/ {
        alias /var/www/on_courses_backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/on_courses_backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/on_courses_backend/oncourses.sock;
    }
}
```

```bash
# Activar sitio y reiniciar Nginx
sudo ln -s /etc/nginx/sites-available/oncourses /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Recolectar archivos estáticos
cd /var/www/on_courses_backend
uv run python manage.py collectstatic --noinput
```

### HTTPS con Certbot (Recomendado)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## 🛠 Tecnologías

<div align="center">

| Categoría | Tecnología |
|---|---|
| **Backend** | ![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django) ![DRF](https://img.shields.io/badge/DRF-3.16-A30000?style=flat-square&logo=django) |
| **Lenguaje** | ![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python) |
| **Base de Datos** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql) |
| **Auth** | ![JWT](https://img.shields.io/badge/JWT-SimpleJWT-000000?style=flat-square&logo=jsonwebtokens) |
| **Documentación** | ![Swagger](https://img.shields.io/badge/Swagger-drf--spectacular-85EA2D?style=flat-square&logo=swagger) |
| **Gestor de Paquetes** | ![uv](https://img.shields.io/badge/uv-0.11-FFD43B?style=flat-square&logo=python) |
| **Servidor** | ![Gunicorn](https://img.shields.io/badge/Gunicorn-Prod-499848?style=flat-square&logo=gunicorn) ![Nginx](https://img.shields.io/badge/Nginx-Reverse--Proxy-009639?style=flat-square&logo=nginx) |
| **Tests** | ![Django Test](https://img.shields.io/badge/TestCase-35%20tests-14854F?style=flat-square&logo=django) |
| **Filtros** | ![django-filter](https://img.shields.io/badge/django--filter-25.1-0D6EFD?style=flat-square) |
| **CORS** | ![CORS](https://img.shields.io/badge/django--cors--headers-4.6-FF6B6B?style=flat-square) |
| **File Upload** | ![Pillow](https://img.shields.io/badge/Pillow-11.1-3776AB?style=flat-square&logo=python) |
| **API Client** | ![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?style=flat-square&logo=postman) |

</div>

---

<div align="center">

**OnCourses API** — *Plataforma de Cursos Online de Tecnología*

Hecho con ❤️ y uno que otro ☕ de Alex López para ti. 

[Reportar Bug](https://github.com/AlexLopezF04/on_courses_backend/issues) · [Solicitar Feature](https://github.com/AlexLopezF04/on_courses_backend/issues) · [Documentación API](/api/docs/)

</div>
