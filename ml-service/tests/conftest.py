"""
conftest.py — Configuración compartida de la suite de pruebas de ml-service.

Responsabilidades:

  1. Añadir `ml-service/` al sys.path para poder hacer `import inference`
     en los tests, sin instalar el paquete ni tocar PYTHONPATH a mano.

  2. Exponer un `client` (TestClient de FastAPI) como fixture de sesión.
     Se usa como context manager para que se dispare el evento `startup`
     de la app y el modelo quede realmente cargado — sin eso, todos los
     endpoints responderían 503.

  3. Saltar la suite completa, con un mensaje accionable, si todavía no
     existe `models/model.pkl`. Así un clon nuevo del repo (o un job de
     CI antes del entrenamiento) reporta "skipped" en vez de una cascada
     de errores que no indican nada útil.

Ejecutar:
    cd ml-service && pytest tests/ -v
"""
from pathlib import Path
import sys

import pytest

ML_SERVICE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH     = ML_SERVICE_DIR / "models" / "model.pkl"

# `import inference` debe resolver a ml-service/inference.py
sys.path.insert(0, str(ML_SERVICE_DIR))


def pytest_collection_modifyitems(config, items):
    """Salta toda la suite si el artefacto del modelo aún no fue generado."""
    if MODEL_PATH.exists():
        return

    skip_marker = pytest.mark.skip(
        reason=(
            f"No se encontró {MODEL_PATH}. "
            f"Ejecute primero `python train.py` desde ml-service/ "
            f"para generar el modelo."
        )
    )
    for item in items:
        item.add_marker(skip_marker)


@pytest.fixture(scope="session")
def client():
    """
    TestClient de FastAPI con el ciclo de vida de la app activo.

    El `with` es imprescindible: dispara `@app.on_event("startup")`, que
    es donde `inference.py` carga model.pkl y model_metadata.json.
    """
    from fastapi.testclient import TestClient
    import inference

    with TestClient(inference.app) as test_client:
        yield test_client
