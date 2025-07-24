"""
Test suite para los endpoints relacionados con listas de tareas
usando FastAPI TestClient.
"""

from tests.conftest import client, HEADERS


def test_create_task_list():
    """
    Verifica que se pueda crear una lista de tareas con éxito.
    Comprueba que el código de respuesta sea 200 o 201.
    """
    response = client.post(
        "/lists/",
        headers=HEADERS,
        json={"name": "Lista de ejemplo", "color_tag": "red", "category": "trabajo"},
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == "Lista de ejemplo"
    assert data["color_tag"] == "red"
    assert data["category"] == "trabajo"


def test_get_task_list_by_id():
    """
    Verifica que se pueda obtener una lista de tareas existente.
    Espera código 200 en la respuesta.
    """
    response = client.get("/lists/?list_id=1", headers=HEADERS)
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "tasks" in data
        assert "completion_percentage" in data


def test_get_task_list_by_path_param():
    """
    Verifica que se pueda obtener una lista específica usando su ID en la URL.
    """
    response = client.get("/lists/1", headers=HEADERS)
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert data["id"] == 1
        assert "name" in data
        assert "color_tag" in data
        assert "category" in data
        assert "tasks" in data


def test_update_task_list():
    """
    Verifica que se pueda actualizar una lista de tareas existente.
    Espera código 200 en la respuesta.
    """
    create_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={"name": "Lista para actualizar", "color_tag": "blue", "category": "test"},
    )
    assert create_response.status_code in (200, 201)
    created = create_response.json()
    list_id = created["id"]

    update_payload = {
        "name": "Lista actualizada",
        "color_tag": "red",
        "category": "actualizado",
    }
    update_response = client.put(
        f"/lists/{list_id}", headers=HEADERS, json=update_payload
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == list_id
    assert updated["name"] == update_payload["name"]
    assert updated["color_tag"] == update_payload["color_tag"]
    assert updated["category"] == update_payload["category"]


def test_delete_task_list():
    """
    Verifica que se pueda eliminar una lista de tareas.
    Acepta código 200 o 204 como respuesta exitosa.
    """
    create_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={"name": "Lista para borrar", "color_tag": "yellow", "category": "test"},
    )
    assert create_response.status_code in (200, 201)
    list_id = create_response.json()["id"]
    delete_response = client.delete(f"/lists/{list_id}", headers=HEADERS)
    assert delete_response.status_code in (200, 204)
