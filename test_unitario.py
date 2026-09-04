from main import validar_nivel


def test_nivel_valido():
    resultado = validar_nivel(5)
    assert resultado is True


def test_nivel_minimo_valido():
    resultado = validar_nivel(1)
    assert resultado is True


def test_nivel_maximo_valido():
    resultado = validar_nivel(10)
    assert resultado is True


def test_nivel_menor_al_minimo():
    resultado = validar_nivel(0)
    assert resultado is False


def test_nivel_mayor_al_maximo():
    resultado = validar_nivel(11)
    assert resultado is False
