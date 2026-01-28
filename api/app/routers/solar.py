# OBJETIVO: endpoints para análisis solar (MVP).
from fastapi import APIRouter
from ..models.solar import SolarAnalysis, SolarRequest
from ..services.solar_service import analyze_solar


router = APIRouter(prefix="/solar", tags=["solar"])


@router.post("/analyze", response_model=SolarAnalysis)
def post_analyze(payload: SolarRequest) -> SolarAnalysis:
    # POST /api/solar/analyze → devuelve análisis solar básico
    return analyze_solar(payload)
