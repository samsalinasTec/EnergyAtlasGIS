# OBJETIVO: calcular potencial solar con datos reales o dummy.
import math
from typing import Dict, List, Tuple

import requests

from ..models.solar import SolarAnalysis, SolarRequest


NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MONTH_DAYS = {
    "JAN": 31,
    "FEB": 28,
    "MAR": 31,
    "APR": 30,
    "MAY": 31,
    "JUN": 30,
    "JUL": 31,
    "AUG": 31,
    "SEP": 30,
    "OCT": 31,
    "NOV": 30,
    "DEC": 31,
}
MONTH_NUM_TO_NAME = {
    "01": "JAN",
    "02": "FEB",
    "03": "MAR",
    "04": "APR",
    "05": "MAY",
    "06": "JUN",
    "07": "JUL",
    "08": "AUG",
    "09": "SEP",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC",
}


def _normalize_monthly_keys(raw: Dict[str, float]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for key, value in raw.items():
        if key in MONTHS:
            normalized[key] = float(value)
        elif key in MONTH_NUM_TO_NAME:
            normalized[MONTH_NUM_TO_NAME[key]] = float(value)
    return normalized


def _daily_to_monthly(daily_avg: Dict[str, float]) -> Dict[str, float]:
    monthly: Dict[str, float] = {}
    for month in MONTHS:
        if month in daily_avg:
            monthly[month] = daily_avg[month] * MONTH_DAYS[month]
    return monthly


def _fetch_nasa_monthly_daily_ghi(latitude: float, longitude: float) -> Dict[str, float]:
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "format": "JSON",
    }
    response = requests.get(NASA_POWER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    raw = (
        data.get("properties", {})
        .get("parameter", {})
        .get("ALLSKY_SFC_SW_DWN", {})
    )
    if not raw:
        raise ValueError("NASA POWER response missing irradiance data")
    return _normalize_monthly_keys(raw)


def _dummy_monthly_daily_ghi(latitude: float) -> Dict[str, float]:
    base = 4.2 + (1 - abs(latitude) / 90) * 1.6
    amplitude = 0.8 + (abs(latitude) / 90) * 0.6
    daily: Dict[str, float] = {}
    for idx, month in enumerate(MONTHS):
        seasonal = amplitude * math.cos((2 * math.pi * (idx - 5)) / 12)
        daily[month] = max(2.5, base + seasonal)
    return daily


def _get_monthly_ghi(
    latitude: float,
    longitude: float,
    data_source: str,
) -> Tuple[Dict[str, float], str, List[str]]:
    notes: List[str] = []
    if data_source == "nasa":
        try:
            daily_avg = _fetch_nasa_monthly_daily_ghi(latitude, longitude)
            return _daily_to_monthly(daily_avg), "nasa", notes
        except Exception:
            notes.append("NASA POWER no respondió; se usó un modelo dummy.")
            daily_avg = _dummy_monthly_daily_ghi(latitude)
            return _daily_to_monthly(daily_avg), "dummy", notes

    daily_avg = _dummy_monthly_daily_ghi(latitude)
    notes.append("Datos dummy generados por estacionalidad simple.")
    return _daily_to_monthly(daily_avg), "dummy", notes


def analyze_solar(request: SolarRequest) -> SolarAnalysis:
    monthly_ghi, source, notes = _get_monthly_ghi(
        request.latitude,
        request.longitude,
        request.data_source,
    )
    annual_ghi = sum(monthly_ghi.values())
    system_capacity_kw = request.area_m2 * request.panel_efficiency
    annual_energy = annual_ghi * request.area_m2 * request.panel_efficiency * request.performance_ratio
    capacity_factor = (
        annual_energy / (system_capacity_kw * 8760)
        if system_capacity_kw > 0
        else 0.0
    )
    monthly_energy = {
        month: ghi * request.area_m2 * request.panel_efficiency * request.performance_ratio
        for month, ghi in monthly_ghi.items()
    }
    assumptions = [
        "Irradiancia mensual calculada desde promedios diarios (kWh/m²/día).",
        "No se considera sombreado ni pérdidas por temperatura.",
        "El cálculo usa GHI sobre plano horizontal (sin corrección por tilt).",
    ]
    assumptions.extend(notes)
    return SolarAnalysis(
        latitude=request.latitude,
        longitude=request.longitude,
        data_source=source,
        annual_ghi_kwh_m2=round(annual_ghi, 2),
        annual_energy_kwh=round(annual_energy, 2),
        system_capacity_kw=round(system_capacity_kw, 2),
        capacity_factor=round(capacity_factor, 4),
        monthly_ghi_kwh_m2={m: round(v, 2) for m, v in monthly_ghi.items()},
        monthly_energy_kwh={m: round(v, 2) for m, v in monthly_energy.items()},
        assumptions=assumptions,
    )
