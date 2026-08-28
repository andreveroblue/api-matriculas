from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API Sistema de Matrículas",
    description="API educativa para realizar pruebas de caja negra",
    version="1.0"
)


class SolicitudMatricula(BaseModel):
    cedula: str
    nivel: int
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

     # RN06
   if datos.cedula is None or datos.nivel is None:
        raise HTTPException(
            status_code=400,
            detail="Los campos cedula y nivel son obligatorios revise"
        )
        
    # RN01
    if datos.nivel < 1 or datos.nivel > 10:
        raise HTTPException(
            status_code=400,
            detail="El nivel académico debe estar entre 1 y 10"
        )

    # RN02
    if datos.impedimento_academico:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento académico"
        )

    # RN03
    if datos.impedimento_financiero:
        raise HTTPException(
            status_code=400,
            detail="El estudiante posee impedimento financiero"
        )

    # RN04
    if datos.numero_asignaturas < 1 or datos.numero_asignaturas > 6:
        raise HTTPException(
            status_code=400,
            detail="El número de asignaturas debe estar entre 1 y 6"
        )

    return {
        "cedula": datos.cedula,
        "estado": "APROBADA",
        "puede_matricularse": True,
        "orden_pago": "GENERADA",
        "mensaje": "El estudiante cumple los requisitos de matrícula"
    }
