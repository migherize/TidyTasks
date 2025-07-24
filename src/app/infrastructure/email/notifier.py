"""
Módulo para enviar notificaciones por correo electrónico.

Contiene funciones simuladas para el envío de invitaciones u otras notificaciones.
"""

import logging

logger = logging.getLogger(__name__)


def notify_assigned_user(assignee_email: str, task_title: str) -> None:
    """
    Simula el envío de una notificación al usuario asignado.
    """
    logger.info(
        "[NOTIFICACIÓN FICTICIA] Se notificó al usuario %s sobre la tarea '%s'.",
        assignee_email,
        task_title,
    )
