"""
test_inference.py — Pruebas del servicio de inferencia de EnergiAI.

Cubre lo que el README de ml-service pide en `tests/`
("pruebas del servicio y validaciones básicas"), sobre la API real
levantada con TestClient — no sobre el modelo aislado:

  · /health responde y reporta el modelo cargado
  · /predict clasifica correctamente perfiles conocidos (una prueba por clase)
  · Las probabilidades son coherentes (suman ~1, la ganadora es la predicha)
  · score_eficiencia: fórmula exacta, rango válido y orden de negocio
  · Validaciones de entrada: campos faltantes o inválidos → 422
  · El contrato de features y el esquema de respuesta quedan congelados

Criterio de diseño: se valida el CONTRATO y las PROPIEDADES, no valores
numéricos exactos del modelo. Un reentrenamiento puede mover una
probabilidad de 0.96 a 0.94 sin que nada esté roto; una prueba que
dependa de ese decimal sería frágil y acabaría ignorándose.

Ejecutar:
    cd ml-service && pytest tests/ -v
"""
import pytest

from inference import FEATURES, PESOS_SCORE

# ── Perfiles de referencia ────────────────────────────────────
# Elegidos en los extremos y el centro del espacio de features para que
# la clase esperada sea estable ante reentrenamientos.
PERFIL_EFICIENTE = {
    "consumo_kwh": 45.0,
    "uso_horario_pico": False,
    "cantidad_equipos": 2,
    "tipo_inmueble": "Casa",
    "horas_alto_consumo": 0,
}

PERFIL_MODERADO = {
    "consumo_kwh": 210.0,
    "uso_horario_pico": False,
    "cantidad_equipos": 10,
    "tipo_inmueble": "Casa",
    "horas_alto_consumo": 190,
}

PERFIL_INEFICIENTE = {
    "consumo_kwh": 950.0,
    "uso_horario_pico": True,
    "cantidad_equipos": 20,
    "tipo_inmueble": "Casa",
    "horas_alto_consumo": 400,
}

CASOS_CONOCIDOS = [
    pytest.param(PERFIL_EFICIENTE,   "Eficiente",   id="eficiente-bajo_consumo"),
    pytest.param(PERFIL_MODERADO,    "Moderado",    id="moderado-consumo_medio"),
    pytest.param(PERFIL_INEFICIENTE, "Ineficiente", id="ineficiente-alto_consumo"),
]

CLASES_VALIDAS = {"Eficiente", "Moderado", "Ineficiente"}


# ══════════════════════════════════════════════════════════════
# /health
# ══════════════════════════════════════════════════════════════
def test_health_responde_ok(client):
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "ok"


def test_health_reporta_modelo_cargado(client):
    """Es el chequeo que usará OCI y el backend antes de integrar."""
    cuerpo = client.get("/health").json()
    assert cuerpo["model_loaded"] is True
    assert set(cuerpo["classes"]) == CLASES_VALIDAS


# ══════════════════════════════════════════════════════════════
# /predict — clasificación
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize("perfil, categoria_esperada", CASOS_CONOCIDOS)
def test_predict_clasifica_correctamente(client, perfil, categoria_esperada):
    respuesta = client.post("/predict", json=perfil)
    assert respuesta.status_code == 200
    assert respuesta.json()["categoria"] == categoria_esperada


@pytest.mark.parametrize("perfil, categoria_esperada", CASOS_CONOCIDOS)
def test_predict_probabilidades_coherentes(client, perfil, categoria_esperada):
    cuerpo = client.post("/predict", json=perfil).json()
    probabilidades = cuerpo["probabilidades"]

    assert set(probabilidades) == CLASES_VALIDAS
    assert sum(probabilidades.values()) == pytest.approx(1.0, abs=0.01)

    # La categoría devuelta debe ser la de mayor probabilidad,
    # y 'probabilidad' debe ser justamente ese máximo.
    clase_top = max(probabilidades, key=probabilidades.get)
    assert clase_top == cuerpo["categoria"]
    assert cuerpo["probabilidad"] == pytest.approx(max(probabilidades.values()), abs=0.01)


# ══════════════════════════════════════════════════════════════
# /predict — score_eficiencia
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize("perfil, _", CASOS_CONOCIDOS)
def test_score_en_rango_valido(client, perfil, _):
    score = client.post("/predict", json=perfil).json()["score_eficiencia"]
    assert 0.0 <= score <= 100.0


@pytest.mark.parametrize("perfil, _", CASOS_CONOCIDOS)
def test_score_coincide_con_la_formula(client, perfil, _):
    """El score debe ser exactamente la combinación lineal documentada."""
    cuerpo = client.post("/predict", json=perfil).json()
    esperado = sum(
        PESOS_SCORE[clase] * prob
        for clase, prob in cuerpo["probabilidades"].items()
    )
    assert cuerpo["score_eficiencia"] == pytest.approx(esperado, abs=0.01)


def test_score_ordena_perfiles_por_eficiencia(client):
    """
    Propiedad de negocio: el score debe ordenar de más a menos eficiente.
    Se validan los extremos con márgenes amplios en vez de valores exactos,
    para que un reentrenamiento no rompa la prueba sin motivo.
    """
    score = lambda perfil: client.post("/predict", json=perfil).json()["score_eficiencia"]

    score_eficiente   = score(PERFIL_EFICIENTE)
    score_moderado    = score(PERFIL_MODERADO)
    score_ineficiente = score(PERFIL_INEFICIENTE)

    assert score_eficiente > 80.0
    assert score_ineficiente < 20.0
    assert score_eficiente > score_moderado > score_ineficiente


def test_score_distingue_dentro_de_la_misma_categoria(client):
    """
    Razón de ser del score continuo: dos perfiles de la misma categoría
    no tienen por qué ser igual de eficientes. Si el score no los
    distingue, no aporta nada sobre la etiqueta.
    """
    apenas_eficiente = {**PERFIL_EFICIENTE, "consumo_kwh": 95.0,
                        "horas_alto_consumo": 40, "cantidad_equipos": 5}

    cuerpo_a = client.post("/predict", json=PERFIL_EFICIENTE).json()
    cuerpo_b = client.post("/predict", json=apenas_eficiente).json()

    if cuerpo_a["categoria"] == cuerpo_b["categoria"]:
        assert cuerpo_a["score_eficiencia"] != cuerpo_b["score_eficiencia"]


# ══════════════════════════════════════════════════════════════
# Validaciones de entrada (contrato Pydantic)
# ══════════════════════════════════════════════════════════════
def test_rechaza_campo_faltante(client):
    incompleto = {k: v for k, v in PERFIL_MODERADO.items() if k != "tipo_inmueble"}
    assert client.post("/predict", json=incompleto).status_code == 422


@pytest.mark.parametrize(
    "campo, valor_invalido, motivo",
    [
        ("consumo_kwh",       -5.0,        "consumo negativo"),
        ("consumo_kwh",        0.0,        "consumo cero (gt=0)"),
        ("cantidad_equipos",   0,          "equipos cero (gt=0)"),
        ("horas_alto_consumo", -1,         "horas negativas (ge=0)"),
        ("tipo_inmueble",      "Castillo", "tipo fuera del Literal"),
    ],
)
def test_rechaza_valores_invalidos(client, campo, valor_invalido, motivo):
    payload = {**PERFIL_MODERADO, campo: valor_invalido}
    respuesta = client.post("/predict", json=payload)
    assert respuesta.status_code == 422, f"Debió rechazar: {motivo}"


def test_acepta_ambos_tipos_de_inmueble(client):
    """Las dos categorías del contrato deben funcionar."""
    for tipo in ("Casa", "Pequeño establecimiento"):
        payload = {**PERFIL_MODERADO, "tipo_inmueble": tipo}
        assert client.post("/predict", json=payload).status_code == 200


# ══════════════════════════════════════════════════════════════
# Contratos congelados
# ══════════════════════════════════════════════════════════════
def test_contrato_de_features_no_cambia_sin_querer():
    """
    Congela las features de entrada. Si alguien cambia una columna en
    train.py sin actualizar inference.py (o al revés), esta prueba falla:
    es la responsabilidad de "mantener consistencia entre features de
    entrenamiento e inferencia" que exige el README de ml-service.
    """
    assert set(FEATURES) == {
        "consumo_kwh",
        "cantidad_equipos",
        "horas_alto_consumo",
        "uso_horario_pico",
        "tipo_inmueble",
    }


def test_pesos_del_score_no_cambian_sin_querer():
    """El backend depende de la escala 0-100; cambiarla es breaking change."""
    assert PESOS_SCORE == {"Eficiente": 100, "Moderado": 50, "Ineficiente": 0}


def test_esquema_de_respuesta_completo(client):
    """El backend consume estos 4 campos: quitar alguno rompe la integración."""
    cuerpo = client.post("/predict", json=PERFIL_MODERADO).json()
    assert set(cuerpo) == {
        "categoria", "probabilidad", "probabilidades", "score_eficiencia"
    }


def test_openapi_documenta_el_score(client):
    """El campo debe aparecer en /docs para que el backend lo vea sin preguntar."""
    esquema = client.get("/openapi.json").json()
    propiedades = esquema["components"]["schemas"]["RespuestaPrediccion"]["properties"]
    assert "score_eficiencia" in propiedades
