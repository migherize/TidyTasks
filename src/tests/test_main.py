"""
Tests para la función `home_page`.

Este módulo contiene pruebas básicas que verifican que la función
`home_page` retorne un diccionario con las claves y valores esperados
de la página de inicio.
"""

from dotenv import load_dotenv

load_dotenv()

from main import home_page  # pylint: disable=wrong-import-position


def test_home_page():
    """
    Prueba la función `home_page` para asegurar que devuelve
    un diccionario con las claves y valores esperados.

    Verifica que:
    - El resultado sea un diccionario.
    - La clave "page" tenga el valor "home".
    - La clave "Version" tenga el valor "1.0".
    - La clave "Update Date" tenga el valor "Jul 23 2025".
    """
    result = home_page()
    assert isinstance(result, dict)
    assert result.get("page") == "home"
    assert result.get("Version") == "1.0"
    assert result.get("Update Date") == "Jul 23 2025"
