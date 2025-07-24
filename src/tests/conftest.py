"""
Configuración común para los tests.

Incluye la carga de variables de entorno,
el cliente de pruebas y los headers de autenticación.
"""

import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

load_dotenv()

client = TestClient(app)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json",
    "Content-Type": "application/json",
}
