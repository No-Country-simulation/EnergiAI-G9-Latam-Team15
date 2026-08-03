"""
test_inference.py
══════════════════════════════════════════════════════════════════
Pruebas del servicio de inferencia — Eficiencia Energética

Cubre lo que pide el README de ml-service ("pruebas del servicio y
validaciones básicas"):

  · Casos conocidos → categoría esperada (uno por cada clase)
  · Coherencia de probabilidades (suman ~1, la clase ganadora es
    la de mayor probabilidad)
  · predict_batch produce el mismo resultado que predict_single
  · Validaciones básicas: campo/columna faltante → ValueError
  · Robustez ante tipo_inmueble no visto en entrenamiento
    ("Apartamento" — solo se entrenó con Casa / Pequeño establecimiento)
  · El contrato de features (EXPECTED_FEATURES) no cambia sin querer

Ejecutar:
    cd ml-service && pytest tests/ -v
    (requiere el modelo ya entrenado en ml-service/models/;
     si no existe, las pruebas se saltan automáticamente — ver conftest.py)
══════════════════════════════════════════════════════════════════
"""
import pandas as pd
import pytest

from inference import predict_single, predict_batch, EXPECTED_FEATURES

CLASES_VALIDAS = {"Eficiente", "Moderado", "Ineficiente"}

# Casos conocidos: los mismos de la demo en inference.py, ya validados
# manualmente contra el modelo entrenado (92.10% accuracy en CV).
CASOS_CONOCIDOS = [
    {
        "id": "eficiente-bajo_consumo",
        "payload": {
            "consumo_kwh": 75.0,
            "uso_horario_pico": False,
            "cantidad_equipos": 2,
            "tipo_inmueble": "Apartamento",  # no vista en entrenamiento
            "horas_alto_consumo": 1,
        },
        "categoria_esperada": "Eficiente",
    },
    {
        "id": "ineficiente-alto_consumo",
        "payload": {
            "consumo_kwh": 850.0,
            "uso_horario_pico": True,
            "cantidad_equipos": 18,
            "tipo_inmueble": "Casa",
            "horas_alto_consumo": 350,
        },
        "categoria_esperada": "Ineficiente",
    },
    {
        "id": "moderado-consumo_medio",
        "payload": {
            "consumo_kwh": 210.0,
            "uso_horario_pico": False,
            "cantidad_equipos": 10,
            "tipo_inmueble": "Casa",
            "horas_alto_consumo": 190,
        },
        "categoria_esperada": "Moderado",
    },
]


# ══════════════════════════════════════════════════════════════
# predict_single — clasificación y coherencia de probabilidades
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize(
    "caso", CASOS_CONOCIDOS, ids=[c["id"] for c in CASOS_CONOCIDOS]
)
def test_predict_single_clasifica_correctamente(caso):
    resultado = predict_single(caso["payload"])
    assert resultado["categoria"] == caso["categoria_esperada"]


@pytest.mark.parametrize(
    "caso", CASOS_CONOCIDOS, ids=[c["id"] for c in CASOS_CONOCIDOS]
)
def test_predict_single_probabilidades_coherentes(caso):
    resultado = predict_single(caso["payload"])
    probs = resultado["probabilidades"]

    # Las 3 clases deben estar presentes en la respuesta
    assert set(probs.keys()) == CLASES_VALIDAS

    # Deben sumar ~1.0 (tolerancia por redondeo a 4 decimales)
    assert sum(probs.values()) == pytest.approx(1.0, abs=0.01)

    # La clase predicha debe ser la de mayor probabilidad
    clase_top = max(probs, key=probs.get)
    assert clase_top == caso["categoria_esperada"]


# ══════════════════════════════════════════════════════════════
# predict_batch — debe coincidir con predict_single
# ══════════════════════════════════════════════════════════════
def test_predict_batch_coincide_con_predict_single():
    df_batch   = pd.DataFrame([c["payload"] for c in CASOS_CONOCIDOS])
    esperadas  = [c["categoria_esperada"] for c in CASOS_CONOCIDOS]

    resultado = predict_batch(df_batch)

    assert list(resultado["categoria_pred"]) == esperadas
    for clase in CLASES_VALIDAS:
        assert f"prob_{clase}" in resultado.columns


def test_predict_batch_falla_si_falta_columna():
    df_incompleto = pd.DataFrame([{
        "consumo_kwh": 100.0,
        "uso_horario_pico": False,
        "cantidad_equipos": 5,
        # faltan 'tipo_inmueble' y 'horas_alto_consumo'
    }])
    with pytest.raises(ValueError):
        predict_batch(df_incompleto)


# ══════════════════════════════════════════════════════════════
# Validaciones básicas
# ══════════════════════════════════════════════════════════════
def test_predict_single_falla_si_falta_campo():
    payload_incompleto = {
        "consumo_kwh": 100.0,
        "uso_horario_pico": False,
        "cantidad_equipos": 5,
        # faltan 'tipo_inmueble' y 'horas_alto_consumo'
    }
    with pytest.raises(ValueError):
        predict_single(payload_incompleto)


def test_expected_features_no_cambia_sin_querer():
    """
    Congela el contrato de features de entrada. Si alguien agrega o
    quita una columna sin actualizar entrenamiento e inferencia a la
    vez, esta prueba debe fallar — es justo la responsabilidad de
    'mantener consistencia entre features de entrenamiento e
    inferencia' que exige el README de ml-service.
    """
    assert EXPECTED_FEATURES == [
        "consumo_kwh",
        "uso_horario_pico",
        "cantidad_equipos",
        "tipo_inmueble",
        "horas_alto_consumo",
    ]
