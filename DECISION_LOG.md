# 🧭 DECISION_LOG.md

Este documento resume las decisiones técnicas más relevantes tomadas durante el desarrollo del backend del proyecto **TidyTasks**.

---

## 1. Lenguaje y Framework

**Decisión:** Utilizar Python 3.10 + FastAPI  
**Motivo:**  
FastAPI permite crear APIs REST robustas con tipado fuerte, documentación automática con OpenAPI (Swagger), y gran rendimiento gracias a Starlette y Pydantic. Python es familiar y altamente productivo para este tipo de backend.

---

## 2. Arquitectura Limpia (Clean Architecture Adaptada)

**Decisión:** Dividir la aplicación en capas: `domain`, `application`, `infrastructure` y `main`  
**Motivo:**  
Para mantener una separación clara de responsabilidades y facilitar testeo, escalabilidad y mantenibilidad. Esta estructura desacopla reglas de negocio de detalles como frameworks, base de datos o adaptadores.

---

## 3. Manejo de Datos: SQLite + ORM

**Decisión:** Usar SQLite como base de datos local y `SQLAlchemy` como ORM.  
**Motivo:**  
SQLite es ideal para pruebas y desarrollo local sin necesidad de configuración adicional. SQLAlchemy permite un mapeo flexible y potente entre clases Python y tablas relacionales.

---

## 4. Manejo de Autenticación

**Decisión:** Implementar autenticación mediante JWT  
**Motivo:**  
Los JWT permiten autenticación stateless (sin sesiones en servidor), ideal para APIs RESTful modernas. Es compatible con escalabilidad horizontal y futuras integraciones frontend o móviles.

---

## 5. Pruebas y Calidad de Código

**Decisión:** Usar `pytest` como framework de testing + `black`, `flake8` y `isort`  
**Motivo:**  
- `pytest` es potente, extensible y fácil de usar.  
- `black`, `flake8` e `isort` aseguran código limpio, ordenado y sin errores comunes.

---

## 6. Contenerización con Docker

**Decisión:** Usar Docker multi-stage con `python:3.10`  
**Motivo:**  
Permite empaquetar la app con sus dependencias en una imagen ligera (`slim-buster`), aislada y portable. Multi-stage reduce el tamaño final del contenedor y separa entorno de build del entorno de ejecución.

---

## 7. Variables de Entorno y Configuración

**Decisión:** Configuración dinámica vía variables de entorno (ENV)  
**Motivo:**  
Facilita el cambio de comportamiento según entorno (`desarrollo`, `producción`, etc.) y evita hardcodeo de credenciales.

---

## 8. Logging estructurado

**Decisión:** Implementar logs en archivos montados por volumen (`/logs`)  
**Motivo:**  
Los logs persistentes son útiles para debugging y monitoreo posterior. Además, separar logs de otras carpetas permite mayor organización y análisis.

---

## 9. Volúmenes en Docker Compose

**Decisión:** Montar las carpetas `src`, `logs`, y `data` como volúmenes  
**Motivo:**  
Permite mantener persistencia y desarrollo en vivo sin reconstruir la imagen. Útil para debugging y pruebas en local.

---

## 10. No uso de Celery ni base de datos externa por simplicidad

**Decisión:** Evitar uso de RabbitMQ, Redis o PostgreSQL en esta fase  
**Motivo:**  
Para mantener el proyecto simple y portable en local. Se considerará usar servicios externos en versiones futuras (ej. PostgreSQL + Redis + Celery para tareas background).

---

## Futuras decisiones posibles

- Implementar frontend en React o Svelte
- Agregar notificaciones reales vía correo o WebSocket
- Sustituir SQLite por PostgreSQL
- Deploy a Render o Railway con Docker

---
