# OBJETIVO: definir endpoints HTTP (como urls+views de Django en uno).
from fastapi import APIRouter, HTTPException
from ..models.country import Country, CountryDetail
from ..services.countries_service import list_countries, get_country

router = APIRouter(prefix="/paises", tags=["paises"])

@router.get("", response_model=list[Country])
def get_list():
    # GET /api/paises → devuelve lista de países
    return list_countries()

@router.get("/{codigo}/ficha", response_model=CountryDetail)
def get_ficha(codigo: str):
    # GET /api/paises/MEX/ficha → devuelve ficha básica del país
    data = get_country(codigo)
    if not data:
        raise HTTPException(status_code=404, detail="pais_no_encontrado")
    return data
