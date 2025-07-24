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
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routers/
│   │   │   └── schemas/
│   │   ├── core/
│   │   ├── domain/
│   │   │   └── models/
│   │   ├── infrastructure/
│   │   │   ├── db/
│   │   │   │   ├── crud/
│   │   │   │   ├── models/
│   │   │   └── email/
│   ├── logs/
│   ├── tests/
│   └── main.py
├── DECISION_LOG.md
├── docker-compose.db.yml
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
```

---

## 📘 Historia de Usuario

> “Como usuario, quiero crear tareas dentro de una lista, actualizarlas, completarlas, filtrarlas por prioridad, y ver qué porcentaje de completitud tiene una lista.”

---

## 🧠 Casos de Uso

### 🗃️ Gestión de Listas

* ✅ Crear, obtener, actualizar y eliminar listas de tareas.
---

### 🗂️ Gestión de Tareas

* ✅ Crear, obtener, actualizar, eliminar tareas.
* 🔁 Cambiar estado (`is_done`).
* 📋 Listar tareas con filtros (`estado`, `prioridad`).
* 📊 Ver porcentaje de completitud de la lista.

## 🧾 Modelos Conceptuales

### Tarea

```json
{
  "id": 1,
  "title": "Preparar reunión",
  "description": "Definir agenda y enviar invitación",
  "priority": "high",
  "is_done": false,
  "assignee_to": "ana@example.com",
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
  "tasks": [
    {
      "id": 1,
      "title": "Preparar reunión",
      "description": "Definir agenda y enviar invitación",
      "priority": "high",
      "is_done": false,
      "assignee_to": "ana@example.com",
      "created_at": "2025-07-23T18:30:00Z",
      "updated_at": "2025-07-23T18:35:00Z",
      "list_id": 10
    },
    {
      "id": 2,
      "title": "Enviar reporte semanal",
      "description": null,
      "priority": "medium",
      "is_done": true,
      "assignee_to": "miguel@example.com",
      "created_at": "2025-07-22T16:00:00Z",
      "updated_at": "2025-07-22T18:00:00Z",
      "list_id": 10
    }
  ],
  "completion_percentage": 50.0
}
```

---

## ⚙️ Requisitos

* Python 3.10+
* Docker
* Docker Compose v2+

---


## 🔧 Configuración de Base de Datos Externa

Puedes usar motores como PostgreSQL o MySQL configurando las siguientes variables en `.env`:

```env
PYTHONPATH=$(pwd)/src
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
cd src/
uvicorn main:app --reload
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

**Base de datos PostgreSQL (modo opcional):**
```bash
docker-compose -f docker-compose.db.yml up --build
```
**Servicio TidyTasks:**
```bash
docker-compose -f docker-compose.yml up --build
```

4. **Accede a la API:**

```
http://localhost:8080/docs
```

---

## Test

Para realizar test de prueba
    ```
    pytest                      # ejecuta los 7 test
    pytest -k test_name         # ejecuta los test 1 a 1
    ```