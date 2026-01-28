# OBJETIVO: definir modelos para análisis solar (request/response).
from typing import Dict, List, Literal
from pydantic import BaseModel, Field


class SolarRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    area_m2: float = Field(..., gt=0)
    panel_efficiency: float = Field(0.20, ge=0, le=1)
    performance_ratio: float = Field(0.80, ge=0, le=1)
    data_source: Literal["nasa", "dummy"] = "nasa"


class SolarAnalysis(BaseModel):
    latitude: float
    longitude: float
    data_source: str
    annual_ghi_kwh_m2: float
    annual_energy_kwh: float
    system_capacity_kw: float
    capacity_factor: float
    monthly_ghi_kwh_m2: Dict[str, float]
    monthly_energy_kwh: Dict[str, float]
    assumptions: List[str]
