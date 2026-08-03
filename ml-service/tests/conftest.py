"""
conftest.py
══════════════════════════════════════════════════════════════════
Configuración compartida para la suite de pytest de ml-service.

  1. Agrega ml-service/app/ al sys.path para poder hacer
         from inference import predict_single, predict_batch
     directamente en los archivos de test, sin instalar el módulo
     como paquete ni tocar PYTHONPATH manualmente.

  2. Si el modelo todavía no fue entrenado (models/ vacío o incompleto),
     las pruebas se SALTAN con un mensaje claro en vez de fallar con
     un traceback confuso — útil en un clon nuevo del repo o en CI
     antes de correr el pipeline de entrenamiento.
══════════════════════════════════════════════════════════════════
"""
import sys
from pathlib import Path

import pytest

TESTS_DIR  = Path(__file__).resolve().parent
ML_SERVICE = TESTS_DIR.parent
APP_DIR    = ML_SERVICE / "app"
MODEL_FILE = ML_SERVICE / "models" / "modelo_eficiencia_energetica.pkl"

sys.path.insert(0, str(APP_DIR))


def pytest_collection_modifyitems(config, items):
    """Salta toda la suite si el modelo aún no ha sido serializado."""
    if not MODEL_FILE.exists():
        skip = pytest.mark.skip(
            reason=(
                f"Modelo no encontrado en {MODEL_FILE}. "
                f"Ejecute primero notebooks/train_pipeline_hibrido_v3.py "
                f"para generar los artefactos en ml-service/models/."
            )
        )
        for item in items:
            item.add_marker(skip)
