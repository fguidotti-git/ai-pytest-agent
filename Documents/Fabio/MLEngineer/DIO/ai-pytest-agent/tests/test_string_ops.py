import pytest

from examples.string_ops import slugify

def test_slugify_success():
    assert slugify("Olá Mundo!") == "ola-mundo"
    assert slugify("Python é incrível") == "python-e-incrivel"
    assert slugify("Teste com espaços    e    caracteres especiais!@#") == "teste-com-espacos-e-caracteres-especiais"
    assert slugify("Açúcar e limão") == "acucar-e-limao"
    assert slugify("   Vários   espaços   ") == "varios-espacos"

def test_slugify_empty_string():
    assert slugify("") == ""

def test_slugify_only_special_characters():
    assert slugify("!@#$%^&*()") == ""

def test_slugify_fails_on_invalid_input():
    with pytest.raises(TypeError, match="slugify() argument must be str, not int"):
        slugify(123)  # Testando com um inteiro

    with pytest.raises(TypeError, match="slugify() argument must be str, not NoneType"):
        slugify(None)  # Testando com None