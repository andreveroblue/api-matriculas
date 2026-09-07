# DEFECTO INTENCIONAL PARA LA PRÁCTICA
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API Sistema de Matrículas",
    description="API educativa para realizar pruebas de caja negra",
    version="1.0"
)


# =========================================================
# MODELO DE DATOS
# =========================================================
# Los cinco campos permiten None para poder probar explícitamente
# los casos de campos obligatorios con valor null.
class SolicitudMatricula(BaseModel):
    cedula: str | None = None
    nivel: int | None = None
    impedimento_academico: bool | None = None
    impedimento_financiero: bool | None = None
    numero_asignaturas: int | None = None


# =========================================================
# FUNCIÓN PARA PRUEBA UNITARIA
# =========================================================
def validar_nivel(nivel):
    return 1 <= nivel <= 10


# =========================================================
# ENDPOINT
# =========================================================
@app.post("/api/matriculas/validar")
def validar_matricula(datos: SolicitudMatricula):

    # -----------------------------------------------------
    # R01 - CAMPOS OBLIGATORIOS
    # -----------------------------------------------------

    if datos.cedula is None:
        raise HTTPException(
            status_code=400,
            detail="La cédula es obligatoria"
        )

    if datos.nivel is None:
        raise HTTPException(
            status_code=400,
            detail="El nivel es obligatorio"
        )

    if datos.numero_asignaturas is None:
        raise HTTPException(
            status_code=400,
            detail="El número de asignaturas es obligatorio"
        )

    if datos.impedimento_academico is None:
        raise HTTPException(
            status_code=400,
            detail="El impedimento académico es obligatorio"
        )

    if datos.impedimento_financiero is None:
        raise HTTPException(
            status_code=400,
            detail="El impedimento financiero es obligatorio"
        )

    # -----------------------------------------------------
    # R02 - NIVEL ACADÉMICO ENTRE 1 Y 10
    # -----------------------------------------------------

    if not validar_nivel(datos.nivel):
        raise HTTPException(
            status_code=400,
            detail="El nivel académico debe estar entre 1 y 10"
        )

    # -----------------------------------------------------
    # R03 - NÚMERO DE ASIGNATURAS ENTRE 1 Y 7
    # -----------------------------------------------------

    if datos.numero_asignaturas < 1 or datos.numero_asignaturas > 7:
        raise HTTPException(
            status_code=400,
            detail="El número de asignaturas debe estar entre 1 y 7"
        )

    # -----------------------------------------------------
    # R06 - DOBLE IMPEDIMENTO
    # AMBOS IMPEDIMENTOS
    # -----------------------------------------------------

    if (
        datos.impedimento_academico is True
        and datos.impedimento_financiero is True
    ):
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento académico"
        )

    # -----------------------------------------------------
    # R04 - IMPEDIMENTO ACADÉMICO
    # -----------------------------------------------------

    if datos.impedimento_academico is True:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento académico"
        )

    # -----------------------------------------------------
    # R05 - IMPEDIMENTO FINANCIERO
    # -----------------------------------------------------

    if datos.impedimento_financiero is True:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento financiero"
        )

    # -----------------------------------------------------
    # R07 - MATRÍCULA APROBADA
    # R08 - ORDEN DE PAGO
    # -----------------------------------------------------

    return {
        "cedula": datos.cedula,
        "nivel": datos.nivel,
        "estado": "APROBADA",
        "puede_matricularse": True,
        "orden_pago": "GENERADA",
        "mensaje": "El estudiante cumple los requisitos de matrícula"
    }


# =========================================================
# ENDPOINT DE COMPROBACIÓN
# =========================================================
@app.get("/")
def inicio():
    return {
        "mensaje": "Sistema de Matrículas funcionando"
    }

