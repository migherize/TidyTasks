# 🧹 TidyTasks

**TidyTasks** es una plataforma ligera para la gestión personal y colaborativa de tareas. Permite a los usuarios organizar proyectos mediante listas, asignar tareas con prioridad, dar seguimiento al progreso, y simular notificaciones por correo.

---

## 📌 Objetivos del Proyecto

* 🧭 Mejorar la organización personal y de equipos mediante tareas categorizadas y con prioridades.
* 🔄 Facilitar la colaboración mediante asignación de responsables y notificaciones.
* ⚙️ Proveer una API REST clara y extensible con FastAPI.
* 🧱 Diseñar con una arquitectura limpia y desacoplada.
* 🔒 Implementar autenticación JWT.
* 🧪 Asegurar calidad con pruebas automatizadas y herramientas de linting.
* 🐳 Facilitar despliegue con soporte Docker.

---

## 🛠 Tecnologías

* Python 3.10+
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* SQLite (dev) / PostgreSQL (producción)
* Pytest
* Docker + Docker Compose
* Logging estructurado

---

## 🚀 Características Principales

* Clean Architecture adaptada.
* CRUD de tareas y listas.
* Autenticación con JWT.
* Pruebas con Pytest.
* Documentación automática (`/docs`, `/redoc`).
* Base de datos SQLite por defecto (PostgreSQL compatible).
* Logs persistentes por volumen.

---

## 📂 Estructura del Proyecto

```
tidytasks-backend/
├── src/
│   ├── application/        # Casos de uso
│   ├── domain/             # Entidades y lógica de negocio
│   ├── infrastructure/     # Repositorios, DB, JWT, etc.
│   └── main/               # Entrypoint FastAPI, rutas y dependencias
├── tests/                  # Pruebas unitarias
├── logs/                   # Carpeta para logs persistentes
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── DECISION_LOG.md
```

---

## 📘 Historia de Usuario

> “Como usuario, quiero crear tareas dentro de una lista, actualizarlas, completarlas, filtrarlas por prioridad, y ver qué porcentaje de completitud tiene una lista.”

---

## 🧠 Casos de Uso

### 🗂️ Gestión de Tareas

* ✅ Crear, obtener, actualizar, eliminar tareas.
* 🔁 Cambiar estado (`is_done`).
* 📋 Listar tareas con filtros (`estado`, `prioridad`).
* 📊 Ver porcentaje de completitud de la lista.

### 🗃️ Gestión de Listas

* ✅ Crear, actualizar y eliminar listas.
* 🎨 Organización visual por `color_tag` o `category`.

---

## 🧾 Modelos Conceptuales

### Tarea

```json
{
  "id": 1,
  "title": "Preparar reunión",
  "description": "Definir agenda y enviar invitación",
  "priority": "high",
  "is_done": false,
  "assignee_to": null,
  "created_at": "2025-07-23T18:30:00Z",
  "updated_at": "2025-07-23T18:35:00Z",
  "list_id": 10
}
```

### Lista

```json
{
  "id": 10,
  "name": "Tareas laborales",
  "color_tag": "#FF5733",
  "category": "trabajo",
  "tasks": [...],
  "completion_percentage": 50.0
}
```

---

## ⚙️ Requisitos

* Python 3.10+
* Docker
* Docker Compose v2+

---

## 🧪 Instalación

### ▶️ Opción 1: Sin Docker

1. **Clona el repositorio:**

```bash
git clone https://github.com/migherize/TidyTasks.git
cd TidyTasks
```

2. **Crea y activa un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instala dependencias:**

```bash
pip install -r requirements.txt
```

4. **Copia y edita `.env`:**

```bash
cp .env.example .env
```

5. **Ejecuta la aplicación:**

```bash
uvicorn src.main:app --reload
```

6. **Accede a la documentación interactiva:**

```
http://127.0.0.1:8000/docs
```

---

### 🐳 Opción 2: Con Docker

1. **Clona el repositorio y entra al directorio:**

```bash
git clone https://github.com/migherize/TidyTasks.git
cd TidyTasks
```

2. **Copia el archivo `.env`:**

```bash
cp .env.example .env
```

3. **Levanta los contenedores:**

```bash
docker compose up --build
```

4. **Accede a la API:**

```
http://localhost:8080/docs
```

---

## 🔧 Configuración de Base de Datos Externa (opcional)

Puedes usar motores como PostgreSQL o MySQL configurando las siguientes variables en `.env`:

```env
DB = "mysql+pymysql"
userDB = "root"
passwordDB = "password"
name_serviceDB = "localhost"
nameBD = "tidytasks"
port = "3306"
```

Formato de conexión ejemplo:

```
postgresql://usuario:contraseña@host:puerto/base_de_datos
```