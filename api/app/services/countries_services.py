# OBJETIVO: lógica de negocio (leer CSV / preparar datos). NO HTTP aquí.
import csv
from typing import List, Optional
from ..models.country import Country, CountryDetail
from ..core.config import settings

CSV_PATH = settings.DATA_DIR / "paises.csv"

def list_countries() -> List[Country]:
    """Lee paises.csv y devuelve lista de países (codigo, nombre)."""
    out = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(Country(codigo=row["CODIGO_PAIS"], nombre=row["NOMBRE_PAIS"]))
    return out

def get_country(codigo: str) -> Optional[CountryDetail]:
    """Busca un país por código (ej: 'MEX')."""
    for c in list_countries():
        if c.codigo.upper() == codigo.upper():
            return CountryDetail(**c.dict())
    return None