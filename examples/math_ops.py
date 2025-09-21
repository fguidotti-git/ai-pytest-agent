def soma(a: float, b: float) -> float:
    return a + b

def subtrai(a: float, b: float) -> float:
    return a - b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b
