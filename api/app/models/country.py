# OBJETIVO: definir la "forma" de los datos (serializador en FastAPI).
from pydantic import BaseModel

class Country(BaseModel):
    codigo: str  # ej: "MEX"
    nombre: str  # ej: "México"

class CountryDetail(Country):
    # Rebanada 2: agrega aquí población, mix energético, etc.
    pass