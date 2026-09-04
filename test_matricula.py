from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# =========================================================
# CP01 - NIVEL VÁLIDO
# =========================================================

def test_matricula_valida():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "APROBADA"
    assert response.json()["puede_matricularse"] is True
    assert response.json()["orden_pago"] == "GENERADA"


# =========================================================
# CP02 - NIVEL MENOR A 1
# =========================================================

def test_nivel_menor_al_minimo():

    datos = {
        "cedula": "0401234567",
        "nivel": -2,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El nivel académico debe estar entre 1 y 10"


# =========================================================
# CP03 - NIVEL MAYOR A 10
# =========================================================

def test_nivel_mayor_al_maximo():

    datos = {
        "cedula": "0401234567",
        "nivel": 12,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El nivel académico debe estar entre 1 y 10"


# =========================================================
# CP04 - ASIGNATURAS = 0
# =========================================================

def test_asignaturas_debajo_del_minimo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 0
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El número de asignaturas debe estar entre 1 y 7"


# =========================================================
# CP05 - LÍMITE MÍNIMO = 1
# =========================================================

def test_asignaturas_limite_minimo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 1
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP06 - CERCA DEL MÍNIMO = 2
# =========================================================

def test_asignaturas_cerca_minimo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 2
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP07 - CERCA DEL MÁXIMO = 6
# =========================================================

def test_asignaturas_cerca_maximo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 6
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP08 - LÍMITE MÁXIMO = 7
# =========================================================

def test_asignaturas_limite_maximo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 7
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200


# =========================================================
# CP09 - SOBRE EL MÁXIMO = 8
# =========================================================

def test_asignaturas_sobre_maximo():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 8
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El número de asignaturas debe estar entre 1 y 7"


# =========================================================
# CP10 - AMBOS IMPEDIMENTOS
# =========================================================

def test_impedimento_academico_y_financiero():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": True,
        "impedimento_financiero": True,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El estudiante posee impedimento académico y financiero"


# =========================================================
# CP11 - SOLO IMPEDIMENTO ACADÉMICO
# =========================================================

def test_impedimento_academico():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": True,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El estudiante posee impedimento académico"


# =========================================================
# CP12 - SOLO IMPEDIMENTO FINANCIERO
# =========================================================

def test_impedimento_financiero():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": True,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El estudiante posee impedimento financiero"


# =========================================================
# CP13 - SIN IMPEDIMENTOS
# =========================================================

def test_sin_impedimentos():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "APROBADA"


# =========================================================
# CP14 - GENERACIÓN DE ORDEN DE PAGO
# =========================================================

def test_generacion_orden_pago():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

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

def test_cedula_obligatoria():

    datos = {
        "cedula": None,
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "La cédula es obligatoria"


# =========================================================
# CP16 - NIVEL OBLIGATORIO
# =========================================================

def test_nivel_obligatorio():

    datos = {
        "cedula": "0401234567",
        "nivel": None,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El nivel es obligatorio"


# =========================================================
# CP17 - IMPEDIMENTO ACADÉMICO OBLIGATORIO
# =========================================================

def test_impedimento_academico_obligatorio():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": None,
        "impedimento_financiero": False,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El impedimento académico es obligatorio"


# =========================================================
# CP18 - IMPEDIMENTO FINANCIERO OBLIGATORIO
# =========================================================

def test_impedimento_financiero_obligatorio():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": None,
        "numero_asignaturas": 3
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El impedimento financiero es obligatorio"


# =========================================================
# CP19 - NÚMERO DE ASIGNATURAS OBLIGATORIO
# =========================================================

def test_numero_asignaturas_obligatorio():

    datos = {
        "cedula": "0401234567",
        "nivel": 5,
        "impedimento_academico": False,
        "impedimento_financiero": False,
        "numero_asignaturas": None
    }

    response = client.post(
        "/api/matriculas/validar",
        json=datos
    )

    assert response.status_code == 400
    assert response.json()["detail"] == \
        "El número de asignaturas es obligatorio"
