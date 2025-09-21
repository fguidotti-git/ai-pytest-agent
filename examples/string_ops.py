import re

def slugify(texto: str) -> str:
    """
    Transforma um texto em um slug simples: minúsculas, sem acentos,
    espaços -> hífen, e remove caracteres inválidos.
    """

    if not isinstance(texto, str):
        raise TypeError(f"slugify argument must be str, not {type(texto).__name__}")


    s = texto.lower()
    s = re.sub(r"[áàâãä]", "a", s)
    s = re.sub(r"[éèêë]", "e", s)
    s = re.sub(r"[íìîï]", "i", s)
    s = re.sub(r"[óòôõö]", "o", s)
    s = re.sub(r"[úùûü]", "u", s)
    s = re.sub(r"ç", "c", s)
    # Use \s (whitespace), não \\s
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s
