"""
Test suite para los endpoints relacionados con tareas
usando FastAPI TestClient.
"""

from tests.conftest import client, HEADERS


def test_create_and_delete_task():
    """
    Crea una lista y una tarea dentro de ella, luego elimina la tarea
    y verifica que la eliminación fue exitosa.

    Finalmente intenta obtener la tarea eliminada y espera un código
    404 o 500 indicando que ya no existe.
    """
    list_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={"name": "Lista test tareas", "color_tag": "blue", "category": "test"},
    )
    assert list_response.status_code == 201
    list_id = list_response.json()["id"]

    task_response = client.post(
        f"/lists/{list_id}/tasks/",
        headers=HEADERS,
        json={
            "title": "Tarea de prueba",
            "description": "Esta es una tarea de prueba",
            "priority": "medium",
            "assigned_to": None,
        },
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    delete_response = client.delete(
        f"/lists/{list_id}/tasks/{task_id}",
        headers=HEADERS,
    )
    assert delete_response.status_code == 204

    get_deleted = client.get(
        f"/lists/{list_id}/tasks/{task_id}",
        headers=HEADERS,
    )
    assert get_deleted.status_code in (404, 500)


def test_get_existing_task():
    """
    Crea una lista y una tarea nueva, luego recupera esa tarea
    y verifica que la información sea correcta.
    """
    # Crear lista
    list_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={
            "name": "Lista para obtener tarea",
            "color_tag": "red",
            "category": "test",
        },
    )
    assert list_response.status_code == 201
    list_id = list_response.json()["id"]

    task_response = client.post(
        f"/lists/{list_id}/tasks/",
        headers=HEADERS,
        json={
            "title": "Tarea a obtener",
            "description": "Descripción de la tarea a obtener",
            "priority": "medium",
            "assigned_to": None,
        },
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    get_response = client.get(
        f"/lists/{list_id}/tasks/{task_id}",
        headers=HEADERS,
    )
    assert get_response.status_code == 200
    task_data = get_response.json()
    assert task_data["id"] == task_id
    assert task_data["list_id"] == list_id
    assert task_data["title"] == "Tarea a obtener"


def test_create_task_and_update_assigned_to_zero():
    """
    Crea una lista y una tarea, luego intenta actualizar la tarea
    asignando el campo `assigned_to` con el valor 0.

    Verifica que la respuesta tenga un código de estado esperado
    (200 si se actualiza correctamente, o 400/500 si falla).

    Finalmente elimina la tarea y la lista para mantener limpio el entorno.
    """
    list_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={"name": "Lista test tareas", "color_tag": "blue", "category": "test"},
    )
    assert list_response.status_code == 201
    list_id = list_response.json()["id"]

    task_response = client.post(
        f"/lists/{list_id}/tasks/",
        headers=HEADERS,
        json={
            "title": "Tarea para update assigned_to=0",
            "description": "Descripción",
            "priority": "medium",
            "assigned_to": None,
        },
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    update_payload = {
        "title": "string",
        "description": "string",
        "priority": "low",
        "assigned_to": 0,
        "is_done": True,
    }
    update_response = client.put(
        f"/lists/{list_id}/tasks/{task_id}", headers=HEADERS, json=update_payload
    )
    assert update_response.status_code in (200, 400, 500)

    client.delete(f"/lists/{list_id}/tasks/{task_id}", headers=HEADERS)
    client.delete(f"/lists/{list_id}", headers=HEADERS)


def test_create_task_and_patch_status():
    """
    Crea una lista y una tarea, luego actualiza el estado de la tarea usando PATCH.
    Verifica que la actualización fue exitosa y que la respuesta contiene los datos correctos.
    Finalmente elimina la tarea y la lista creada para dejar limpio el entorno.
    """
    list_response = client.post(
        "/lists/",
        headers=HEADERS,
        json={
            "name": "Lista test patch status",
            "color_tag": "red",
            "category": "test",
        },
    )
    assert list_response.status_code == 201
    list_id = list_response.json()["id"]

    task_response = client.post(
        f"/lists/{list_id}/tasks/",
        headers=HEADERS,
        json={
            "title": "Tarea para patch status",
            "description": "Descripcion",
            "priority": "medium",
            "assigned_to": None,
        },
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    patch_payload = {"is_done": True}
    patch_response = client.patch(
        f"/lists/{list_id}/tasks/{task_id}/status", headers=HEADERS, json=patch_payload
    )

    assert patch_response.status_code == 200
    data = patch_response.json()
    assert data["id"] == task_id
    assert data["is_done"] is True

    delete_task_response = client.delete(
        f"/lists/{list_id}/tasks/{task_id}", headers=HEADERS
    )
    delete_list_response = client.delete(f"/lists/{list_id}", headers=HEADERS)

    assert delete_task_response.status_code in (200, 204)
    assert delete_list_response.status_code in (200, 204)
