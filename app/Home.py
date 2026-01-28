# OBJETIVO: MVP solar con inputs, mapa 2D/3D y KPIs básicos.
import math
import random
from typing import Dict, List

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

from config import API_BASE_URL


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def _offset_lat_lon(lat: float, lon: float, dx_m: float, dy_m: float) -> tuple[float, float]:
    lat_factor = 110_574
    lon_factor = 111_320 * math.cos(math.radians(lat)) + 1e-6
    return lat + (dy_m / lat_factor), lon + (dx_m / lon_factor)


def _generate_buildings(
    latitude: float,
    longitude: float,
    radius_km: float,
    count: int,
) -> List[Dict]:
    radius_m = radius_km * 1000
    seed = int((latitude + 90) * 1000) * 100000 + int((longitude + 180) * 1000)
    random.seed(seed)
    buildings: List[Dict] = []
    for idx in range(count):
        r = radius_m * math.sqrt(random.random())
        theta = random.random() * 2 * math.pi
        dx = r * math.cos(theta)
        dy = r * math.sin(theta)
        center_lat, center_lon = _offset_lat_lon(latitude, longitude, dx, dy)
        size_m = random.uniform(20, 80)
        height_m = random.uniform(6, 30)
        half = size_m / 2
        p1 = _offset_lat_lon(center_lat, center_lon, -half, -half)
        p2 = _offset_lat_lon(center_lat, center_lon, half, -half)
        p3 = _offset_lat_lon(center_lat, center_lon, half, half)
        p4 = _offset_lat_lon(center_lat, center_lon, -half, half)
        buildings.append(
            {
                "id": idx,
                "polygon": [
                    [p1[1], p1[0]],
                    [p2[1], p2[0]],
                    [p3[1], p3[0]],
                    [p4[1], p4[0]],
                ],
                "height_m": height_m,
            }
        )
    return buildings


def _fetch_solar(payload: Dict) -> Dict | None:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/solar/analyze",
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"No se pudo calcular el análisis solar: {exc}")
        return None


def _make_deck(
    latitude: float,
    longitude: float,
    radius_km: float,
    buildings: List[Dict],
) -> pdk.Deck:
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=12 if radius_km <= 2 else 11 if radius_km <= 4 else 10,
        pitch=45,
        bearing=0,
    )
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": latitude, "lon": longitude}],
            get_position="[lon, lat]",
            get_radius=radius_km * 1000,
            radius_units="meters",
            get_fill_color=[30, 144, 255, 60],
            get_line_color=[30, 144, 255, 200],
            stroked=True,
            filled=True,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": latitude, "lon": longitude}],
            get_position="[lon, lat]",
            get_radius=40,
            radius_units="meters",
            get_fill_color=[255, 99, 71, 200],
        ),
        pdk.Layer(
            "PolygonLayer",
            data=buildings,
            get_polygon="polygon",
            get_elevation="height_m",
            get_fill_color=[200, 0, 80, 140],
            get_line_color=[255, 255, 255, 80],
            pickable=True,
            extruded=True,
        ),
    ]
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style=pdk.map_styles.CARTO_LIGHT,
        tooltip={"text": "Edificio dummy\nAltura: {height_m} m"},
    )


def _build_insights(analysis: Dict) -> List[str]:
    messages = []
    if analysis["annual_ghi_kwh_m2"] >= 1800:
        messages.append("El sitio tiene irradiancia anual alta para PV.")
    if analysis["capacity_factor"] >= 0.20:
        messages.append("Capacidad factor estimada competitiva para PV.")
    if analysis["system_capacity_kw"] >= 10:
        messages.append("El área útil permite un sistema > 10 kW.")
    if not messages:
        messages.append("Sitio con potencial moderado; revisa datos reales.")
    return messages


st.set_page_config(page_title="Atlas Solar", layout="wide")
st.title("Atlas Solar — MVP")
st.caption("Inputs a la izquierda. Mapa 2D/3D y KPIs en pantalla.")

with st.sidebar:
    st.header("Inputs")
    latitude = st.number_input("Latitud", value=19.4326, format="%.6f")
    longitude = st.number_input("Longitud", value=-99.1332, format="%.6f")
    radius_km = st.slider("Radio de análisis (km)", 0.5, 5.0, 1.5, 0.1)
    area_m2 = st.number_input("Área útil PV (m²)", min_value=1.0, value=120.0, step=10.0)
    panel_eff = st.slider("Eficiencia panel", 0.12, 0.25, 0.20, 0.01)
    pr = st.slider("Performance ratio", 0.60, 0.90, 0.80, 0.01)
    data_source = st.selectbox("Fuente de irradiancia", ["nasa", "dummy"])
    buildings_count = st.slider("Edificios dummy", 20, 200, 60, 10)
    run = st.button("Analizar", type="primary")

buildings = _generate_buildings(latitude, longitude, radius_km, buildings_count)
deck = _make_deck(latitude, longitude, radius_km, buildings)

st.pydeck_chart(deck, use_container_width=True)

analysis = st.session_state.get("analysis")
if run:
    with st.spinner("Calculando análisis solar..."):
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "area_m2": area_m2,
            "panel_efficiency": panel_eff,
            "performance_ratio": pr,
            "data_source": data_source,
        }
        analysis = _fetch_solar(payload)
        if analysis:
            st.session_state["analysis"] = analysis

if analysis:
    st.subheader("KPIs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("GHI anual (kWh/m²)", analysis["annual_ghi_kwh_m2"])
    col2.metric("Energía anual (kWh)", analysis["annual_energy_kwh"])
    col3.metric("Capacidad (kW)", analysis["system_capacity_kw"])
    col4.metric("Capacity factor", analysis["capacity_factor"])

    st.subheader("Producción mensual (kWh)")
    monthly_energy = analysis["monthly_energy_kwh"]
    chart_df = pd.DataFrame(
        {
            "Mes": MONTHS,
            "Energía (kWh)": [monthly_energy.get(m, 0) for m in MONTHS],
        }
    ).set_index("Mes")
    st.bar_chart(chart_df, height=250)

    st.subheader("Insights rápidos (MVP)")
    for msg in _build_insights(analysis):
        st.write(f"- {msg}")

    with st.expander("Supuestos usados"):
        for item in analysis.get("assumptions", []):
            st.write(f"- {item}")
else:
    st.info("Configura los inputs y presiona 'Analizar' para ver resultados.")
