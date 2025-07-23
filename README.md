# 🧹 TidyTasks

**TidyTasks** es una plataforma ligera para la gestión personal y colaborativa de tareas. Permite a los usuarios organizar sus proyectos mediante listas, añadir tareas con prioridad, hacer seguimiento de su progreso, asignar responsables y simular notificaciones por correo.

---

## 📌 Objetivos del Proyecto

**TidyTasks** nace con el propósito de ofrecer una solución sencilla pero extensible para la gestión de tareas personales y colaborativas. Los principales objetivos del proyecto son:

- 🧭 **Mejorar la organización personal y de equipos** mediante listas de tareas categorizadas, tareas con prioridades y seguimiento del progreso.
- 🔄 **Facilitar la colaboración** en equipos reducidos o proyectos personales con la asignación de tareas a usuarios y simulación de notificaciones.
- ⚙️ **Proveer una API REST robusta, clara y extensible**, desarrollada con FastAPI, que sirva tanto como backend funcional como base para futuras integraciones (web o mobile).
- 🧱 **Construir una arquitectura limpia y desacoplada**, organizada en capas (Domain, Application, Infrastructure) que permita mantener, escalar y probar el sistema de forma eficiente.
- 🔒 **Implementar autenticación con JWT y control de acceso**, permitiendo escalar a modelos multiusuario en versiones futuras.
- 🧪 **Garantizar la calidad del código y la estabilidad**, mediante pruebas automatizadas, linters y herramientas de formateo.
- 🐳 **Asegurar una fácil distribución y despliegue**, con soporte para entornos Dockerizados listos para desarrollo y producción.

---

## 📘 Historia de Usuario: Gestión de Tareas

> “Como usuario, quiero poder crear tareas dentro de una lista, actualizarlas, cambiar su estado (completa/incompleta), filtrarlas por prioridad o estado, y ver qué porcentaje de la lista está completado para poder organizar mejor mi tiempo y prioridades.”

---

## 🧠 Casos de Uso

### 🗂️ Gestión de Tareas

- ✅ **Crear una tarea:**
  - Campos requeridos: `title`, `priority` (`low`, `medium`, `high`)
  - Opcionales: `description`, `assignee`
  - Estado inicial: `pendiente` (`is_done = false`)
  - Asociada a una lista

- 🔍 **Obtener una tarea específica**
  - Por `task_id` dentro de una lista

- ✏️ **Actualizar tarea:**
  - Cambios en `title`, `description`, `priority`, `is_done`, `assignee`

- 🗑️ **Eliminar tarea**

- 🔁 **Cambiar estado** de la tarea (`toggle is_done`)

- 📋 **Listar tareas** dentro de una lista con filtros:
  - Filtros: `estado` (`is_done = true/false`) y `priority`
  - Campo adicional: `% de completitud` de la lista

---

### 🗃️ Gestión de Listas

- ✅ Crear, actualizar y eliminar listas de tareas
- Cada lista puede tener un campo `color_tag` (ej: `#FF5733`) o `category` (ej: `"trabajo"`, `"personal"`) para su organización visual

---

## 🧾 Modelo de Tarea (Conceptual)

```json
{
  "id": 1,
  "title": "Preparar reunión",
  "description": "Definir agenda y enviar invitación",
  "priority": "high",
  "is_done": false,
  "assignee": null,
  "created_at": "2025-07-23T18:30:00Z",
  "updated_at": "2025-07-23T18:35:00Z",
  "list_id": 10
}

```
## 🧾 Modelo de Tarea (Conceptual)

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
      "assignee": null,
      "created_at": "2025-07-23T18:30:00Z",
      "updated_at": "2025-07-23T18:35:00Z"
    },
    {
      "id": 2,
      "title": "Enviar reporte mensual",
      "description": null,
      "priority": "medium",
      "is_done": true,
      "assignee": "juan@example.com",
      "created_at": "2025-07-20T10:00:00Z",
      "updated_at": "2025-07-21T15:45:00Z"
    }
  ],
  "completion_percentage": 50.0
}
```
