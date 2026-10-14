from src.utils.dates import formatear_mes

def test_formatea_anio_mes():
    assert formatear_mes("2025-09") == "Sep 2025"

def test_acepta_fecha_completa():
    assert formatear_mes("2026-04-25") == "Apr 2026"

def test_none_devuelve_present():
    assert formatear_mes(None) == "Present"