class SolicitudMatricula(BaseModel):
    cedula: str | None = None
    nivel: int | None = None
    impedimento_academico: bool
    impedimento_financiero: bool
    numero_asignaturas: int


@app.post("/api/matriculas/validar")
def validar_matricula(datos: SolicitudMatricula):

    # RN06 - Cédula obligatoria
    if datos.cedula is None:
        raise HTTPException(
            status_code=400,
            detail="La cédula es obligatoria "
        )

    # RN07 - Nivel obligatorio
    if datos.nivel is None:
        raise HTTPException(
            status_code=400,
            detail="El nivel es obligatorio"
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
