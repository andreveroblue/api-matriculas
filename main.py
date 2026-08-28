from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API Sistema de Matrículas",
    description="API educativa para realizar pruebas de caja negra",
    version="1.0"
)


class SolicitudMatricula(BaseModel):
    cedula: str | None = None
    nivel: int | None = None
    impedimento_academico: bool
    impedimento_financiero: bool
    numero_asignaturas: int


@app.get("/")
def inicio():
    return {
        "sistema": "Sistema de Matrículas",
        "estado": "API funcionando"
    }


@app.post("/api/matriculas/validar")
def validar_matricula(datos: SolicitudMatricula):

    # RN06 - Cédula y nivel son obligatorios
    if datos.cedula is None or datos.nivel is None:
        raise HTTPException(
            status_code=400,
            detail="Los campos cédula y nivel son obligatorios"
        )

    # RN01 - Validación del nivel
    if datos.nivel < 1 or datos.nivel > 10:
        raise HTTPException(
            status_code=400,
            detail="El nivel académico debe estar entre 1 y 10"
        )

    # RN02 - Impedimento académico
    if datos.impedimento_academico:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento académico"
        )

    # RN03 - Impedimento financiero
    if datos.impedimento_financiero:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento financiero"
        )

    # RN04 - Número de asignaturas
    if datos.numero_asignaturas < 1 or datos.numero_asignaturas > 6:
        raise HTTPException(
            status_code=400,
            detail="El número de asignaturas debe estar entre 1 y 6"
        )

    # Matrícula aprobada
    return {
        "cedula": datos.cedula,
        "nivel": datos.nivel,
        "estado": "APROBADA",
        "puede_matricularse": True,
        "orden_pago": "GENERADA",
        "mensaje": "El estudiante cumple los requisitos de matrícula"
    }
