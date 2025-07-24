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
  "assigned_to": 1,
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
      "assigned_to": 2,
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
      "assigned_to": null,
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

Antes de instalar y ejecutar la aplicación, **debes tener una base de datos creada y accesible**. La aplicación es compatible con múltiples motores de base de datos relacionales.

### Motores compatibles:

* **Relacionales:** PostgreSQL, MySQL, MariaDB, SQLite

Puedes apoyarte en herramientas visuales como **MySQL Workbench**, **pgAdmin**, **DBeaver**, entre otras, para facilitar la creación y gestión de la base de datos.

---

### 1. Crear la Base de Datos

Crea una base de datos vacía con el nombre que desees, utilizando tu motor preferido. Una vez creada, deberás establecer la conexión mediante variables de entorno.

La conexión se construye utilizando una URL estándar que SQLAlchemy interpreta automáticamente. Algunos ejemplos:

```bash
# PostgreSQL
postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>

# MySQL (con PyMySQL)
mysql+pymysql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>
```

---

### 2. Variables de Entorno Requeridas

Debes definir las siguientes variables en un archivo `.env` antes de ejecutar la aplicación:

```env
PYTHONPATH=$(pwd)/src

# Tipo de base de datos (por ejemplo: postgresql o mysql+pymysql)
DB=postgresql

# Usuario y contraseña
USERDB=tidytasks
PASSWORDDB=tidytasks

# Host y puerto
NAME_SERVICEDB=localhost
PORT=5432

# Nombre de la base de datos
NAMEDB=tidytasks

# JWT
SECRET_KEY=devsecretkey123
ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzUzMzcwNTQzfQ.PbLCQuiczV6-cQd-rTGGIgcrWVqRGX0daxFrGs3pURU

```

La aplicación utilizará estos valores para construir automáticamente la URL de conexión:

```text
<DB>://<USERDB>:<PASSWORDDB>@<NAME_SERVICEDB>:<PORT>/<NAMEDB>
```

Ejemplo real con PostgreSQL:

```text
postgresql://tidytasks:tidytasks@localhost:5432/tidytasks
```

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

#  Para aplicar formateo automático
black 
flake8 
isort 

# Se recomienda configurar pre-commit
pre-commit install
```

4. **Copia y edita `.env`:**

```bash
cp .env.example .env
```

**Base de datos PostgreSQL (modo opcional):**

Puedes levantar un contenedor de PostgreSQL fácilmente con Docker si no tienes una base de datos local configurada:

```bash
docker-compose -f docker-compose.db.yml up --build
```

Esto iniciará una instancia de PostgreSQL con las credenciales definidas en el archivo `docker-compose.db.yml`. El contenedor estará accesible desde tu aplicación mediante las variables de entorno.

> ⚠️ **Nota obligatoria**:
> Si prefieres usar tu propia base de datos local o remota, **es obligatorio** definir correctamente las siguientes variables en tu archivo `.env` para que la aplicación pueda conectarse.

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

Igual que en la Opcion 1, debe usarse una DB obligatoriamente.

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

## Endpoints principales

Aquí tienes una captura con los endpoints disponibles en la API:

![Captura Endpoints](docs/endpoints_capture.png)

## Tests

Este proyecto incluye pruebas automatizadas con **pytest** para validar el correcto funcionamiento de los endpoints principales.

### Ejecutar los tests

1. Asegúrate de tener instaladas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

2. Ejecuta las pruebas con pytest:

```bash
pytest
```

---

### Colección Postman

Para pruebas manuales, se provee una colección de Postman que facilita la exploración y verificación de los endpoints.

#### Variables de entorno necesarias

Antes de usar la colección, debes configurar dos variables en el entorno de Postman:

* `{{url_tidy_task}}`: URL base donde está corriendo la API (ejemplo: `http://localhost:8000`)
* `{{access_token}}`: Token Bearer para autenticación en los endpoints protegidos (Endpoint RegisterUserAuth y LoginUserAuth)

---

**Nota:** La correcta configuración de estas variables es necesaria para que las peticiones funcionen correctamente desde Postman.

---
