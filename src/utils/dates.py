import re

MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# YYYY-MM o YYYY-MM-DD, con mes 01-12 y día 01-31
FORMATO_FECHA = re.compile(r"^\d{4}-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$")


def es_fecha_valida(valor: str) -> bool:
    return bool(FORMATO_FECHA.match(valor))


def formatear_mes(valor: str | None) -> str:
    if not valor:
        return "Present"
    partes = valor.split("-")
    anio, mes = int(partes[0]), int(partes[1])
    return f"{MESES[mes - 1]} {anio}"
