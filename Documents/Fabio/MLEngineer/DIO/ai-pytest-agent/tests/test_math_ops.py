import pytest
from examples.math_ops import soma, subtrai, divide

def test_soma():
    assert soma(1, 2) == 3, "Deve retornar 3 para soma de 1 e 2"
    assert soma(-1, 1) == 0
    assert soma(2.5, 0.5) == 3.0

def test_subtrai():
    assert subtrai(5, 3) == 2, "Deve retornar 2 para subtração de 5 e 3"
    assert subtrai(0, 2) == -2
    assert subtrai(2.5, 0.5) == 2.0

def test_divide():
    assert divide(6, 3) == 2, "Deve retornar 2 para divisão de 6 por 3"

def test_divide_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
