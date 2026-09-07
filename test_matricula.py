from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def datos_base():
    return {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }


# =========================================================
# CP01 - NIVEL VÁLIDO
# =========================================================
def test_CP01_nivel_valido():
    datos = datos_base()

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "APROBADA"


# =========================================================
# CP02 - LÍMITE INFERIOR INVÁLIDO = 0
# =========================================================
def test_CP02_nivel_menor_al_minimo():
    datos = datos_base()
    datos["nivel"] = 0

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El nivel académico debe estar entre 1 y 10"
    )


# =========================================================
# CP03 - LÍMITE SUPERIOR INVÁLIDO = 11
# =========================================================
def test_CP03_nivel_mayor_al_maximo():
    datos = datos_base()
    datos["nivel"] = 11

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El nivel académico debe estar entre 1 y 10"
    )


# =========================================================
# CP04 - ASIGNATURAS = 0
# =========================================================
def test_CP04_asignaturas_debajo_del_minimo():
    datos = datos_base()
    datos["numero_asignaturas"] = 0

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El número de asignaturas debe estar entre 1 y 7"
    )


# =========================================================
# CP05 - LÍMITE MÍNIMO = 1
# =========================================================
def test_CP05_asignaturas_limite_minimo():
    datos = datos_base()
    datos["numero_asignaturas"] = 1

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP06 - CERCA DEL MÍNIMO = 2
# =========================================================
def test_CP06_asignaturas_cerca_minimo():
    datos = datos_base()
    datos["numero_asignaturas"] = 2

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP07 - CERCA DEL MÁXIMO = 6
# =========================================================
def test_CP07_asignaturas_cerca_maximo():
    datos = datos_base()
    datos["numero_asignaturas"] = 6

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP08 - LÍMITE MÁXIMO = 7
# =========================================================
def test_CP08_asignaturas_limite_maximo():
    datos = datos_base()
    datos["numero_asignaturas"] = 7

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP09 - SOBRE EL MÁXIMO = 8
# =========================================================
def test_CP09_asignaturas_sobre_maximo():
    datos = datos_base()
    datos["numero_asignaturas"] = 8

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El número de asignaturas debe estar entre 1 y 7"
    )

# =========================================================
# CP10 - DOBLE IMPEDIMENTO
# =========================================================
def test_CP10_doble_impedimento():
    datos = datos_base()
    datos["impedimento_academico"] = True
    datos["impedimento_financiero"] = True

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El estudiante posee impedimento académico y financiero"
    )


# =========================================================
# CP11 - SOLO IMPEDIMENTO ACADÉMICO
# =========================================================
def test_CP11_impedimento_academico():
    datos = datos_base()
    datos["impedimento_academico"] = True

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El estudiante posee impedimento académico"
    )


# =========================================================
# CP12 - SOLO IMPEDIMENTO FINANCIERO
# =========================================================
def test_CP12_impedimento_financiero():
    datos = datos_base()
    datos["impedimento_financiero"] = True

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El estudiante posee impedimento financiero"
    )


# =========================================================
# CP13 - SIN IMPEDIMENTOS
# =========================================================
def test_CP13_sin_impedimentos():
    datos = datos_base()

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "APROBADA"


# =========================================================
# CP14 - GENERACIÓN DE ORDEN DE PAGO
# =========================================================
def test_CP14_generacion_orden_pago():
    datos = datos_base()

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200
    assert response.json()["puede_matricularse"] is True
    assert response.json()["orden_pago"] == "GENERADA"


# =========================================================
# CP15 - CÉDULA OBLIGATORIA
# =========================================================
def test_CP15_cedula_obligatoria():
    datos = datos_base()
    datos["cedula"] = None

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "La cédula es obligatoria"
    )


# =========================================================
# CP16 - NIVEL OBLIGATORIO
# =========================================================
def test_CP16_nivel_obligatorio():
    datos = datos_base()
    datos["nivel"] = None

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El nivel es obligatorio"
    )


# =========================================================
# CP17 - IMPEDIMENTO ACADÉMICO OBLIGATORIO
# =========================================================
def test_CP17_impedimento_academico_obligatorio():
    datos = datos_base()
    datos["impedimento_academico"] = None

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El impedimento académico es obligatorio"
    )


# =========================================================
# CP18 - IMPEDIMENTO FINANCIERO OBLIGATORIO
# =========================================================
def test_CP18_impedimento_financiero_obligatorio():
    datos = datos_base()
    datos["impedimento_financiero"] = None

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El impedimento financiero es obligatorio"
    )


# =========================================================
# CP19 - NÚMERO DE ASIGNATURAS OBLIGATORIO
# =========================================================
def test_CP19_numero_asignaturas_obligatorio():
    datos = datos_base()
    datos["numero_asignaturas"] = None

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El número de asignaturas es obligatorio"
    )
