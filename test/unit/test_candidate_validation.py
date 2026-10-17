import pytest
from pydantic import ValidationError

from src.models.candidate import Experience, Leadership


def experiencia(**cambios):
    base = dict(
        title="Dev", company="X", location="Monterrey, NL",
        start_date="2024-01", end_date="2025-05",
    )
    base.update(cambios)
    return base


def test_acepta_anio_mes():
    assert Experience(**experiencia()).start_date == "2024-01"


def test_acepta_end_date_vacio():
    assert Experience(**experiencia(end_date=None)).end_date is None


@pytest.mark.parametrize("valor", ["2025/09", "2025-13", "25-09", "2025-9", "2025-00"])
def test_rechaza_formatos_invalidos(valor):
    with pytest.raises(ValidationError):
        Experience(**experiencia(start_date=valor))


def test_rechaza_fin_antes_de_inicio():
    with pytest.raises(ValidationError):
        Experience(**experiencia(start_date="2025-05", end_date="2024-01"))


def test_leadership_acepta_fecha_completa():
    lider = Leadership(
        title="Datathon", organization="Tec", date="2026-04-25", description="x",
    )
    assert lider.date == "2026-04-25"


def test_leadership_rechaza_formato_invalido():
    with pytest.raises(ValidationError):
        Leadership(title="T", organization="O", date="25/04/2026", description="x")